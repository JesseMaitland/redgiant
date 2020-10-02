from typing import Tuple, List
from redscope.schema_introspection.db_objects.constraint import Constraint
from redscope.schema_introspection.formatters.base_formatter import DDLFormatter


class ConstraintFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> List[Constraint]:
        return [Constraint(name=constraint[4],
                           schema=constraint[0],
                           table=constraint[1],
                           ddl=constraint[3]) for constraint in raw_ddl]
