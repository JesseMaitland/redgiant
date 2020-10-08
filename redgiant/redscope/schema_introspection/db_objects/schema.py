from typing import Dict, List
from redgiant.redscope.schema_introspection.db_objects.ddl import DDL


class SchemaBox:

    def __init__(self,
                 tables: Dict = None,
                 views: Dict = None,
                 udfs: Dict = None,
                 procedures: Dict = None) -> None:

        self._tables = {t.name: t for t in tables} if tables else {}
        self._views = {v.name: v for v in views} if views else {}
        self._udfs = {u.name: u for u in udfs} if udfs else {}
        self._procedures = {p.name: p for p in procedures} if procedures else {}

    def tables(self) -> Dict[str, DDL]:
        return self._tables

    def table(self, name: str) -> DDL:
        return self._tables[name]

    def views(self) -> List[DDL]:
        return list(self._views.values())

    def view(self, name: str) -> DDL:
        return self._views[name]

    def udfs(self) -> List[DDL]:
        return list(self._udfs.values())

    def udf(self, name: str) -> DDL:
        return self._udfs[name]

    def procedures(self) -> List[DDL]:
        return list(self._procedures.values())

    def procedure(self, name: str) -> DDL:
        return self._procedures[name]


class Schema(DDL):

    def __init__(self, name: str):
        super().__init__(name=name, schema=name)
        self.schema_box: SchemaBox = None

    @property
    def get(self) -> SchemaBox:
        return self.schema_box

    def file_name(self) -> str:
        return f"{self.name}.sql"

    def create(self) -> str:
        return f"CREATE SCHEMA {self.name};"

    def create_if_not_exist(self) -> str:
        return f"CREATE SCHEMA IF NOT EXISTS {self.name};"

    def drop(self) -> str:
        return f"DROP SCHEMA {self.name};"

    def drop_if_exist(self) -> str:
        return f"DROP SCHEMA IF EXISTS {self.name};"

    def drop_if_exists_cascade(self) -> str:
        return f"{self.drop_if_exist} CASCADE;"

    def set_schema_box(self, schema_box: SchemaBox):
        self.schema_box = schema_box
