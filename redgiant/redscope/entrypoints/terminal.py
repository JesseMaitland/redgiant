from redgiant.terminal.entrypoint import RedGiantEntryPoint
from redgiant.redscope.project.file_paths import FilePaths
from redgiant.redscope.schema_introspection.db_introspection import introspect_redshift, DbIntrospection

_allowed_introspection_choices = DbIntrospection.allowed_db_objects.copy()
_allowed_introspection_choices.remove('constraints')
_allowed_introspection_choices.append('all')


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
        db_catalog = introspect_redshift(db_connection, self.args.entity)

