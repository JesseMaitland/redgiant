import shutil
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from jinja2 import PackageLoader, Environment

from .ymlobj import User, Role, Group


class GateKeeper:

    def __init__(self, users: Dict[str, User], roles: Dict[str, Role], groups: Dict[str, Group]) -> None:

        for role in roles.values():
            role.set_groups(groups)

        for user in users.values():
            user.set_roles(roles)

        self.items = {
            'users': users,
            'roles': roles,
            'groups': groups
        }

    def get_user(self, name: str) -> User:
        return self.items['users'][name]

    def get_users(self) -> List[User]:
        return list(self.items['users'].values())


