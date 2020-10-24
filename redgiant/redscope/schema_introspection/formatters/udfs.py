from typing import Tuple, List
from redgiant.redscope.schema_introspection.db_objects.udf import UDF
from redgiant.redscope.schema_introspection.formatters.base_formatter import DDLFormatter


class UdfFormatter(DDLFormatter):

    def __init__(self):
        super().__init__()

    def format(self, raw_ddl: Tuple[str]) -> List[UDF]:

        udfs = []
        for ddl in raw_ddl:
            schema, name, content = ddl
            udf = UDF(schema=schema, name=name, ddl=content)
            udfs.append(udf)
        return udfs
