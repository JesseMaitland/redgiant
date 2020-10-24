from redgiant.redscope.project import RedScopeSingleActionEntryPoint
# from redgiant.redscope.project.file_paths import FilePaths
from redgiant.redscope.schema_introspection.db_introspection import introspect_redshift, DbIntrospection

_allowed_introspection_choices = DbIntrospection.allowed_db_objects.copy()
# _allowed_introspection_choices.remove('constraints')


class Introspect(RedScopeSingleActionEntryPoint):

    discover = True

    entry_point_args = {
        ('--entity', '-e'): {
            'help': 'the name of the database object you would like to introspect. Default will introspect everything',
            'choices': _allowed_introspection_choices,
            'default': None
        }
    }

    def action(self) -> None:
        db_connection = self.config.get_db_connection('redshift')
        redshift_schema = introspect_redshift(db_connection, self.args.entity, True)

        for schema in redshift_schema.schemas().values():
            schema_path = self.project.get_ddl_filepath(schema)
            schema_path.parent.mkdir(parents=True, exist_ok=True)
            schema_path.touch(exist_ok=True)
            schema_path.write_text(schema.create())

            for ddl in schema.items():
                if ddl.__class__.__name__.lower() in ['schema', 'table', 'view', 'procedure', 'udf']:
                    path = self.project.get_ddl_filepath(ddl)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.touch(exist_ok=True)
                    path.write_text(ddl.create())


        t = redshift_schema.schema('atomic').get.table('events')
        print(t.constraints[0].create())
