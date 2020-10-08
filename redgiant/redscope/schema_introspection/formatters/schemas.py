from typing import Tuple, Dict
from redgiant.redscope.schema_introspection.db_objects.schema import Schema
from redgiant.redscope.schema_introspection.formatters.base_formatter import DDLFormatter


class SchemaFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> Dict[str, Schema]:
        return {schema[0]: Schema(name=schema[0]) for schema in raw_ddl}
