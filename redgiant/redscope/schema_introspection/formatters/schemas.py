from typing import Tuple, Dict
from redgiant.redscope.schema_introspection.db_objects.schema import Schema
from redgiant.redscope.schema_introspection.formatters.base_formatter import DDLFormatter


class SchemaFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> Dict[str, Schema]:
        template = self.template_env.get_template('schema.yml')

        schemas = {}
        for schema in raw_ddl:
            content = template.render(schema=schema[0])
            ddl_map = self.map_ddl(content)
            schema_obj = Schema(name=schema[0], ddl_map=ddl_map)
            schemas[schema_obj.name] = schema_obj
        return schemas
