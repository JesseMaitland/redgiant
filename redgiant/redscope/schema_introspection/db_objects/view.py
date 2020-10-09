from redgiant.redscope.schema_introspection.db_objects.ddl import DDL


class View(DDL):

    def __init__(self, schema: str, name: str, **kwargs):
        super().__init__(name=name, schema=schema, **kwargs)

    def file_name(self) -> str:
        return f"{self.schema}.{self.name}.sql"
