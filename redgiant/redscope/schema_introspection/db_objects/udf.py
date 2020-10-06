from redgiant.redscope.schema_introspection.db_objects.ddl import DDL


class UDF(DDL):

    def __init__(self, schema: str, name: str, ddl: str):
        self.schema = schema
        self.ddl = ddl
        super().__init__(name)

    @property
    def file_name(self) -> str:
        return f"{self.name}.sql"

    @property
    def create(self) -> str:
        return self.ddl

    @property
    def create_if_not_exist(self) -> str:
        return self.create

    @property
    def drop(self) -> str:
        return f"DROP FUNCTION {self.schema}.{self.name};"

    @property
    def drop_if_exist(self) -> str:
        return f"DROP FUNCTION IF EXISTS {self.schema}.{self.name};"

    @property
    def drop_if_exists_cascade(self) -> str:
        return f"DROP FUNCTION IF EXISTS {self.schema}.{self.name};"
