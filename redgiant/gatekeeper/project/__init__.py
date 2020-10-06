import yaml
from pathlib import Path
from typing import Dict, List
from redgiant.terminal.project import RedGiantProject
from redgiant.terminal.entrypoint import RedGiantEntryPoint


class Group(yaml.YAMLObject):
    yaml_tag = "!Group"

    def __init__(self, name: str, schemas: List[str], permissions: List[str]) -> None:
        self.name = name
        self.schemas = schemas
        self.permissions = permissions


class Role(yaml.YAMLObject):
    yaml_tag = "!Role"

    def __init__(self, name: str, groups: List[str]) -> None:
        self.name = name
        self.groups = groups
        self._groups = {}

    def set_groups(self, groups: Dict[str, Group]) -> None:
        self._groups = {}
        for group_name, group in groups.items():
            if group_name in self.groups:
                self._groups[group_name] = group

    def get_groups(self) -> Dict[str, Group]:
        return self._groups


class User(yaml.YAMLObject):
    yaml_tag = '!User'

    def __init__(self, name: str, password: str, roles: List[str], is_system_user: bool = False,
                 owns_schemas: List[str] = None) -> None:
        self.name = name
        self.password = password
        self.roles = roles
        self._roles = {}
        self.is_system_user = is_system_user
        self.owns_schemas = owns_schemas or []

    def set_roles(self, roles: Dict[str, Role]) -> None:
        self._roles = {}
        for role_name, role in roles.items():
            if role_name in self.roles:
                self._roles[role_name] = role

    def get_roles(self) -> Dict[str, Role]:
        return self._roles

    @property
    def groups(self) -> List[Group]:
        groups = []
        for role in self._roles.values():
            for group in role.get_groups().values():
                groups.append(group)
        return list(set(groups))

    @property
    def owned_schemas(self) -> List[str]:
        return self.owns_schemas


class GateKeeper:

    def __init__(self, users: Dict[str, User], roles: Dict[str, Role], groups: Dict[str, Group]) -> None:

        for role in roles.values():
            role.set_groups(groups)

        for user in users.values():
            user.set_roles(roles)

        self.db_objects = {
            'users': users,
            'roles': roles,
            'groups': groups
        }

    def get_user(self, name: str) -> User:
        return self.db_objects['users'][name]

    def get_users(self) -> List[User]:
        return list(self.db_objects['users'].values())


class GateKeeperProject(RedGiantProject):

    def __init__(self, root_name: str):
        super().__init__(root_name=root_name)

        gatekeeper = 'gatekeeper'
        configs = 'configs'
        users = 'users'
        ownership = 'ownership'
        groups = 'groups'
        audits = 'audits'
        roles = 'roles'

        self.dirs = {
            configs: self.root / gatekeeper / configs,
            users: self.root / gatekeeper / users,
            ownership: self.root / gatekeeper / ownership,
            groups: self.root / gatekeeper / groups,
            audits: self.root / gatekeeper / audits
        }

        self.config_files = {
            users: self.root / gatekeeper / configs / f"{users}.yml",
            groups: self.root / gatekeeper / configs / f"{groups}.yml",
            roles: self.root / gatekeeper / configs / f"{roles}.yml"
        }

    def init_project(self):
        self.create_root()
        self.create_dirs()
        self.create_config_files()

    def create_config_files(self):
        template_env = self.get_jinja_env('gatekeeper')
        for f in self.config_files.values():
            content = template_env.get_template(f.name).render()
            f.touch(exist_ok=True)
            f.write_text(content)

    def create_dirs(self):
        for d in self.dirs.values():
            d.mkdir(exist_ok=True, parents=True)

    def get_dir(self, name: str) -> Path:
        return Path(self.dirs[name]).absolute()

    def get_gatekeeper(self) -> GateKeeper:
        config = {}
        for config_name, config_path in self.config_files.items():
            c = yaml.load_all(config_path.open(), Loader=yaml.FullLoader)
            config[config_name] = {i.name: i for i in c}
        return GateKeeper(**config)


class GateKeeperEntryPoint(RedGiantEntryPoint):

    def __init__(self):
        super().__init__()
        self.project = GateKeeperProject(self.config.get_project_root())



