# # standard lib
# from datetime import datetime
# from typing import List
#
# # 3rd party deps
# from redgiant.terminal.entrypoint import EntryPoint
# from prettytable import PrettyTable
# from redgiant.scope.schema_introspection.db_introspection import introspect_redshift
# from redgiant.scope.schema_introspection.db_objects import DbCatalog
#
# # project deps
# from redgiant.gatekeeper.project import ProjectContext
# from redgiant.gatekeeper.tools import group_ownership
#
#
# class AuditUsers(EntryPoint):
#
#     entry_point_args = {
#         ('--create-migration', '-c'): {
#             'help': 'set this flag if you would like to generate a ddl script',
#             'action': 'store_true',
#             'default': False
#         },
#
#         ('--print', '-p'): {
#             'help': """set this flag if you would like to print the audit table to the terminal.
#             No changes will take effect.""",
#             'action': 'store_true',
#             'default': False
#         }
#     }
#
#     def __init__(self, config_path):
#         super(AuditUsers, self).__init__(config_path)
#         self.pc = ProjectContext()
#         self.je = self.pc.get_jinja_env()
#
#         db_connection = self.rsterm.get_db_connection('redscope')
#         self.dbc: DbCatalog = introspect_redshift(db_connection, verbose=True)
#         db_connection.close()
#
#     def run(self) -> None:
#
#         user_mappings = self.get_user_mapping()
#
#         if self.cmd_args.print:
#             self.print_table(user_mappings)
#
#         if self.cmd_args.create_migration:
#             self.create_drop_user_migration(user_mappings)
#
#     def get_user_mapping(self) -> List[List[str]]:
#         redshift_users = [u.name for u in self.dbc.users]
#         gatekeeper_users = [u.name for u in self.pc.get_config().get_users()]
#
#         redshift_users.sort()
#         gatekeeper_users.sort()
#
#         redshift_mapping = [(x, x, 'x') if x in gatekeeper_users else (x, '', '') for x in redshift_users]
#         gatekeeper_mapping = [(x, x, 'x') if x in redshift_users else ('', x, 'x') for x in gatekeeper_users]
#
#         mapping = list(set(redshift_mapping + gatekeeper_mapping))
#         mapping.sort(key=lambda x: x[0] + x[1])
#
#         return mapping
#
#     @staticmethod
#     def print_table(user_mappings: List):
#
#         table = PrettyTable()
#         table.field_names = ['redshift', 'gatekeeper', 'is valid']
#
#         for user_mapping in user_mappings:
#             table.add_row(user_mapping)
#
#         print(table)
#         exit()
#
#     def create_drop_user_migration(self, user_mappings: List):
#         invalid_user_names = [x[0] or x[1] for x in user_mappings if not x[2]]
#         invalid_users = []
#
#         for m in self.dbc.membership:
#             if m.name in invalid_user_names:
#                 invalid_users.append(m)
#
#         template = self.je.get_template('drop.sql')
#         self.pc.clean_dir('user_audit')
#         file = self.pc.dirs.get('user_audit') / self.pc.get_audit_file_name('users', 'audit')
#         content = template.render(invalid_users=invalid_users, dt=datetime.now().replace(microsecond=0))
#         file.write_text(content)
#
#
# class AuditOwnership(EntryPoint):
#
#     def __init__(self, config_path):
#         self.pc = ProjectContext()
#         self.je = self.pc.get_jinja_env()
#         self.co = self.pc.get_config()
#         super(AuditOwnership, self).__init__(config_path)
#         db_connection = self.rsterm.get_db_connection('redscope')
#         self.dbc = introspect_redshift(db_connection, 'ownership', verbose=True)
#         db_connection.close()
#
#     def run(self) -> None:
#
#         self.pc.clean_dir('ownership_audit')
#         p_dir = self.pc.dirs['ownership_audit']
#         template = self.je.get_template('ownership_audit.sql')
#         ownership = group_ownership(self.dbc)
#         dt = datetime.now().replace(microsecond=0)
#
#         for user, db_objects in ownership.items():
#             content = template.render(**{'user': user, 'db_objects': db_objects, 'dt': dt})
#             file_name = self.pc.get_audit_file_name(user, 'audit')
#             fp = p_dir / file_name
#             fp.touch()
#             fp.write_text(content)
