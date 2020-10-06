from typing import Tuple, List
from redgiant.redscope.schema_introspection.db_objects.group import Group
from redgiant.redscope.schema_introspection.formatters.base_formatter import DDLFormatter


class GroupFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> List[Group]:
        return [Group(name=group[0]) for group in raw_ddl]
