import shutil
from pathlib import Path
from jinja2 import PackageLoader, Environment


class RedGiantProject:

    def __init__(self, root_name: str):

        root = Path.cwd().absolute() / root_name

        # gatekeeper dirs
        gatekeeper_root = root / 'gatekeeper'

        gatekeeper = {
            'configs': gatekeeper_root / 'configs',
            'ddl': gatekeeper_root / 'ddl',
            'ownership': gatekeeper_root / 'ownership',
            'audits': gatekeeper_root / 'audits',
        }

        self.dirs = {
            'gatekeeper': gatekeeper
        }

#        self.config_files = {
#            'groups': configs / 'groups.yml',
#            'users': configs / 'users.yml',
#            'roles': configs / 'roles.yml'
#        }

    def init_project(self, feature: str):
        for d in self.dirs[feature].values():
            d.mkdir(exist_ok=True, parents=True)

    def get_dir(self, feature: str, name: str, *args):
        base = self.dirs[feature][name]

        if args:
            base = base.joinpath('/'.join(args))

        return base
