from typing import Tuple, List
from redgiant.redscope.schema_introspection.db_objects.udf import UDF
from redgiant.redscope.schema_introspection.formatters.base_formatter import DDLFormatter


class UdfFormatter(DDLFormatter):

    def __init__(self, raw_ddl: Tuple[str] = None):
        self.raw_ddl = raw_ddl or ()

    def format(self, raw_ddl: Tuple[str]) -> List[UDF]:
        self.raw_ddl = raw_ddl
        return [UDF(schema=ddl[0], name=ddl[1], ddl=ddl[2]) for ddl in self.raw_ddl]
