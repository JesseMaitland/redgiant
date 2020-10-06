import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from jinja2 import PackageLoader, Environment


class RedGiantProject(ABC):

    def __init__(self, root_name: str):
        self.root = Path.cwd() / root_name
        self.dirs = {}

    def create_root(self):
        self.root.mkdir(exist_ok=True, parents=True)

    @abstractmethod
    def get_dir(self, *args, **kwargs) -> Path:
        pass

    def clean_dir(self, name: str) -> None:
        dir_path = self.get_dir(name)
        shutil.rmtree(dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_jinja_env(name: str) -> Environment:
        loader = PackageLoader(package_name='redgiant', package_path=f'templates/{name}')
        return Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
