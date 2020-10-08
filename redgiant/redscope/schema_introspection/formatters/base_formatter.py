from abc import ABC, abstractmethod
from typing import List, Tuple
from redgiant.redscope.schema_introspection.db_objects.ddl import DDL


class DDLFormatter(ABC):

    @abstractmethod
    def format(self, raw_ddl: Tuple[str]) -> List[DDL]:
        pass
