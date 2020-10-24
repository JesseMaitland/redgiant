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

    def ddl(self) -> List[DDL]:
        return [i for value in self.__dict__.values() for i in value.values()]

    def tables(self) -> Dict[str, DDL]:
        return self._tables

    def table(self, name: str) -> DDL:
        return self._tables.get(name, DDL.empty())

    def views(self) -> Dict[str, DDL]:
        return self._views

    def view(self, name: str) -> DDL:
        return self._views.get(name, DDL.empty())

    def udfs(self) -> List[DDL]:
        return list(self._udfs.values())

    def udf(self, name: str) -> DDL:
        return self._udfs[name]

    def procedures(self) -> List[DDL]:
        return list(self._procedures.values())

    def procedure(self, name: str) -> DDL:
        return self._procedures[name]


class Schema(DDL):

    def __init__(self, name: str, ddl_map: Dict[str, str]):
        super().__init__(name=name, schema=name, ddl_map=ddl_map)
        self._schema_box: SchemaBox = SchemaBox()

    @property
    def get(self) -> SchemaBox:
        return self._schema_box

    def file_name(self) -> str:
        return f"{self.name}.sql"

    def set_schema_box(self, schema_box: SchemaBox):
        self._schema_box = schema_box

    def ddl(self) -> List[DDL]:
        return self._schema_box.ddl()
