import yaml
from io import StringIO
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from redgiant.redscope.schema_introspection.db_objects.ddl import DDL
from redgiant.redscope.project import RedScopeProject


class DDLFormatter(ABC):

    def __init__(self):
        self.template_env = RedScopeProject.get_jinja_env('redscope')

    @abstractmethod
    def format(self, raw_ddl: Tuple[str]) -> List[DDL]:
        pass

    @staticmethod
    def map_ddl(content: str) -> Dict[str, str]:
        return yaml.safe_load(StringIO(content))
