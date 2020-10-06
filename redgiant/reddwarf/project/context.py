import os
import yaml
from pathlib import Path
from typing import List, Dict, Callable
from jinja2 import Environment, PackageLoader


class ProjectContext:
    _template_path = Path(__file__).absolute().parent.parent / "templates"

    def __init__(self):
        root = Path.cwd().absolute() / "red-dwarf"
        configs = 'configs'
        rendered = 'rendered'

        self._paths = {
            'root': root,
            configs: root / configs,
            rendered: root / rendered
        }

        self.parse_config: Callable = None

    @property
    def template_path(self) -> Path:
        return self._template_path

    @property
    def unload_template_path(self) -> Path:
        return self._template_path / "unload.sql"

    def set_config_parser(self, config_parser: Callable) -> None:
        self.parse_config = config_parser

    def get_dir(self, name: str) -> Path:
        return self._paths[name]

    def init_project(self):
        self.create_project_dirs()

    def create_project_dirs(self):

        if self.get_dir('root').exists():
            raise FileExistsError("Red Dwarf project already exists!")
        else:
            for name, path in self._paths.items():
                path.mkdir(parents=True, exist_ok=True)

    def create_config(self, name: str) -> None:
        template = Path(self._template_path / "config_template.yml").read_text()
        config_path = self.get_dir('configs')
        config_file = config_path / f"{name}.yml"

        if config_file.exists():
            raise FileExistsError("config file names must be unique.")
        else:
            config_file.touch(exist_ok=True)
            config_file.write_text(template)

    def list_configs(self) -> List[str]:
        return [f.name for f in self.get_dir('configs').glob('**/*.yml')]

    def list_config_paths(self) -> List[Path]:
        return [f for f in self.get_dir('configs').glob('**/*.yml')]

    def get_configs(self) -> Dict[str, Path]:
        return {p.name.split('.')[0]: p for p in self.get_dir('configs').glob('**/*.yml')}

    def get_config(self, name: str) -> Dict[str, Path]:
        config = self.get_configs()[name]
        return {name: config}

    def create_rendered_dir(self, name: str) -> None:
        rendered_root = self.get_dir('rendered')
        rendered_dir = rendered_root / name
        rendered_dir.mkdir(exist_ok=True, parents=True)

    def list_rendered_dirs(self):
        rendered_root = self.get_dir('rendered')
        return {d: Path(rendered_root / d).absolute() for d in os.listdir(rendered_root.as_posix())}

    def get_rendered_dir(self, name: str) -> Path:
        return self.list_rendered_dirs()[name]

    @staticmethod
    def save_rendered_templates(rendered_dir: Path, templates: Dict[str, str]) -> None:
        for file_name, content in templates.items():
            path = rendered_dir / file_name
            path.touch(exist_ok=True)
            path.write_text(content)

    @staticmethod
    def get_jinja_env() -> Environment:
        return Environment(
            loader=PackageLoader(package_name='red_dwarf', package_path='templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )
