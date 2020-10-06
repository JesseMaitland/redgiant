from typing import Tuple, List
from redgiant.redscope.schema_introspection.db_objects.ownership import Ownership
from redgiant.redscope.schema_introspection.formatters.base_formatter import DDLFormatter


class OwnershipFormatter(DDLFormatter):

    def __init__(self, raw_ddl: Tuple[str] = None):
        self.raw_ddl = raw_ddl or ()

    def format(self, raw_ddl: Tuple[str]) -> List[Ownership]:
        self.raw_ddl = raw_ddl
        return [Ownership(schema=ddl[0],
                          name=ddl[1],
                          owner=ddl[2],
                          signature=ddl[3],
                          db_obj_type=ddl[4])
                for ddl in self.raw_ddl]
