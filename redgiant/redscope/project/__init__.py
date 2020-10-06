from redgiant.terminal.project import RedGiantProject
from redgiant.terminal.entrypoint import RedGiantEntryPoint


class RedScopeProject(RedGiantProject):

    def __init__(self, root_name: str) -> None:
        super().__init__(root_name)

        redscope = 'redscope'
        schemas = 'schemas'
        permissions = 'permissions'

        self.dirs = {
            redscope: self.root / redscope,
            schemas: self.root / redscope / schemas,
            permissions: self.root / redscope / permissions
        }

    def get_dir(self, name: str):
        return self.dirs[name]

    def init_project(self):
        for path in self.dirs.values():
            path.mkdir(parents=True, exist_ok=True)

    def clean_project(self):
        self.clean_dir('redscope')


class RedScopeEntryPoint(RedGiantEntryPoint):

    def __init__(self):
        super().__init__()
        self.project = RedScopeProject(self.config.get_project_root())

