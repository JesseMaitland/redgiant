from redgiant.redscope.schema_introspection.db_objects.ddl import DDL


class UDF(DDL):

    def __init__(self, schema: str, name: str, ddl: str):
        self.ddl = ddl
        super().__init__(name=name, schema=schema)

    def file_name(self) -> str:
        return f"{self.name}.sql"

    def create(self) -> str:
        return self.ddl

    def create_if_not_exist(self) -> str:
        return self.create

    def drop(self) -> str:
        return f"DROP FUNCTION {self.schema}.{self.name};"

    def drop_if_exist(self) -> str:
        return f"DROP FUNCTION IF EXISTS {self.schema}.{self.name};"

    def drop_if_exists_cascade(self) -> str:
        return f"DROP FUNCTION IF EXISTS {self.schema}.{self.name};"
