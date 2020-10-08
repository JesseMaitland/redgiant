from redgiant.terminal.entrypoint import RedGiantEntryPoint
# from redgiant.redscope.project.file_paths import FilePaths
from redgiant.redscope.schema_introspection.db_introspection import introspect_redshift_v2, DbIntrospection

_allowed_introspection_choices = DbIntrospection.allowed_db_objects.copy()
_allowed_introspection_choices.remove('constraints')


class Introspect(RedGiantEntryPoint):

    entry_point_args = {
        ('--entity', '-e'): {
            'help': 'the name of the database object you would like to introspect. Default will introspect everything',
            'choices': _allowed_introspection_choices,
            'default': None
        }
    }

    def cmd_redshift(self):
        db_connection = self.config.get_db_connection('redshift')
        redshift_schema = introspect_redshift_v2(db_connection, self.args.entity)

        print(redshift_schema.schema('stage').get.table('campaigns').create())
