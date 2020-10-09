from typing import Tuple, List
from redgiant.redscope.schema_introspection.db_objects.view import View
from redgiant.redscope.schema_introspection.formatters.base_formatter import DDLFormatter


class ViewFormatter(DDLFormatter):

    def __init__(self):
        super().__init__()

    def format(self, raw_ddl: Tuple[str]) -> List[View]:

        template = self.template_env.get_template('view.yml')

        views = []
        for ddl in raw_ddl:
            schema, name, content = ddl
            content = template.render(schema=schema, name=name, content=content)
            ddl_map = self.map_ddl(content)
            view = View(schema=schema, name=name, ddl_map=ddl_map)
            views.append(view)

        return views
