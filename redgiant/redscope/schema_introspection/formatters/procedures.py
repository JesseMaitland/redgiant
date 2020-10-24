from typing import Tuple, List
from redgiant.redscope.schema_introspection.db_objects.procedure import Procedure
from redgiant.redscope.schema_introspection.formatters.base_formatter import DDLFormatter


class ProcedureFormatter(DDLFormatter):

    def __init__(self):
        super().__init__()

    def format(self, raw_ddl: Tuple[str]) -> List[Procedure]:

        template = self.template_env.get_template('procedure.yml')

        procedures = []
        for ddl in raw_ddl:
            schema, name, content = ddl
            content = template.render(schema=schema, name=name, content=content)
            ddl_map = self.map_ddl(content)
            procedure = Procedure(schema=schema, name=name, ddl_map=ddl_map)
            procedures.append(procedure)

        return procedures
