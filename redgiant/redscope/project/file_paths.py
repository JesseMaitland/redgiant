from pathlib import Path
from redgiant.redscope.project.project_context import ProjectContext
from redgiant.redscope.schema_introspection.db_objects.ddl import DDL
from redgiant.redscope.schema_introspection.db_objects.db_catalog import DbCatalog


class FilePaths:

    def __init__(self):
        self.dir_context = ProjectContext()

    def make_dir_and_file(self, ddl: DDL, path: Path):
        path.mkdir(exist_ok=True, parents=True)
        path = path / ddl.file_name
        path.touch(exist_ok=True)
        path.write_text(ddl.create_if_not_exist)

    def save_files(self, db_catalog: DbCatalog, verbose: bool = True):

        for name in db_catalog.file_object_names:
            ddls = db_catalog.get_db_objects(name)

            for ddl in ddls:

                # TODO: clean this up
                if name in ['schemas']:
                    path = self.dir_context.get_dir(name)
                    path = path / ddl.name
                    self.make_dir_and_file(ddl, path)

                elif name in ['tables', 'views', 'udfs', 'ownership']:
                    path = self.dir_context.get_dir('schemas')
                    path = path / ddl.schema / name
                    self.make_dir_and_file(ddl, path)

                elif name == 'groups':
                    path = self.dir_context.get_dir('permissions')
                    path = path / name
                    self.make_dir_and_file(ddl, path)

                elif name in ['users', 'membership']:
                    path = self.dir_context.get_dir('permissions')
                    path = path / 'users' / ddl.name
                    self.make_dir_and_file(ddl, path)

                else:
                    path = self.dir_context.get_dir(name)
                    self.make_dir_and_file(ddl, path)
