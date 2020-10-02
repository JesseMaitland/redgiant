from rsterm import EntryPoint
from redscope.env.file_paths import FilePaths
from redscope.schema_introspection.db_introspection import introspect_redshift, DbIntrospection

_allowed_introspection_choices = DbIntrospection.allowed_db_objects.copy()
_allowed_introspection_choices.remove('constraints')
_allowed_introspection_choices.append('all')


class IntrospectRedshift(EntryPoint):

    entry_point_args = {

        ('--entity', '-e'): {
            'help': 'the name of the database object you would like to introspect. Default value is all',
            'choices': _allowed_introspection_choices,
            'type': str,
            'default': 'all'
        }
    }

    def run(self) -> None:

        db_connection = self.rsterm.get_db_connection('redscope')

        if self.cmd_args.entity == 'all':
            db_catalog = introspect_redshift(db_connection, verbose=True)
        else:
            db_catalog = introspect_redshift(db_connection, self.cmd_args.entity, verbose=True)

        file_paths = FilePaths()
        file_paths.save_files(db_catalog)
        exit()


class PrintTable(EntryPoint):

    def run(self) -> None:
        db_connection = self.rsterm.get_db_connection('redscope')
        db_catalog = introspect_redshift(db_connection, 'tables')

        for table in db_catalog.tables:
            print(table.create_external_table('foo_bar'))
