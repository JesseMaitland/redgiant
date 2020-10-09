from pathlib import Path
from typing import Dict

class DDL:

    def __init__(self, name: str, ddl_map: Dict[str, str], schema: str = None):

        allowed_kwargs = ['create', 'create_if_not_exists', 'drop', 'drop_if_exists', 'drop_cascade', 'create_external', 'create_or_replace']

        self.name = name
        self.schema = schema

        for key, value in ddl_map.items():
            if key in allowed_kwargs:
                setattr(self, f"_{key}", value)
            else:
                raise ValueError(f"DDL got unexpected key word argument {key}")

    def __bool__(self) -> bool:
        return True if self.name else False

    @classmethod
    def empty(cls):
        return cls('', '')

    def file_name(self) -> str:
        raise NotImplementedError

    def file_key(self) -> Path:
        raise NotImplementedError

    def create(self) -> str:
        return getattr(self, '_create', '')

    def create_if_not_exists(self) -> str:
        return getattr(self, '_create_if_not_exists', '')

    def drop(self) -> str:
        return getattr(self, '_drop', '')

    def drop_if_exists(self) -> str:
        return getattr(self, '_drop_if_exists', '')

    def drop_cascade(self) -> str:
        return getattr(self, '_drop_cascade', '')

    def create_external(self) -> str:
        return getattr(self, '_create_external', '')

    def create_or_replace(self) -> str:
        return getattr(self, '_create_or_replace', '')
