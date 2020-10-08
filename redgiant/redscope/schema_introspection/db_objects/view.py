from redgiant.redscope.schema_introspection.db_objects.ddl import DDL


class View(DDL):

    def __init__(self, schema: str, name: str, ddl: str):
        self.ddl = ddl
        super().__init__(name=name, schema=schema)

    def file_name(self) -> str:
        return f"{self.name}.sql"

    def create(self) -> str:
        return f"CREATE VIEW {self.schema}.{self.name} AS \n {self.ddl};"

    def create_if_not_exist(self) -> str:
        return f"CREATE OR REPLACE VIEW {self.schema}.{self.name} AS \n {self.ddl};"

    def drop(self) -> str:
        return f"DROP VIEW {self.schema}.{self.name};"

    def drop_if_exist(self) -> str:
        return f"DROP VIEW IF EXISTS {self.schema}.{self.name};"
