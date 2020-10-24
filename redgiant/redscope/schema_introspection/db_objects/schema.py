from typing import Dict, List
from redgiant.redscope.schema_introspection.db_objects.ddl import DDL


class SchemaBox:

    def __init__(self,
                 tables: Dict = None,
                 views: Dict = None,
                 udfs: Dict = None,
                 procedures: Dict = None,
                 constraints: Dict = None) -> None:

        self._tables = {t.name: t for t in tables} if tables else {}
        self._views = {v.name: v for v in views} if views else {}
        self._udfs = {u.name: u for u in udfs} if udfs else {}
        self._procedures = {p.name: p for p in procedures} if procedures else {}
        self._constraints = {c.name: c for c in constraints} if constraints else {}

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

    def udfs(self) -> Dict[str, DDL]:
        return self._udfs

    def udf(self, name: str) -> DDL:
        return self._udfs.get(name, DDL.empty())

    def procedures(self) -> Dict[str, DDL]:
        return self._procedures

    def procedure(self, name: str) -> DDL:
        return self._procedures.get(name, DDL.empty())

    def constraints(self) -> Dict[str, DDL]:
        return self._constraints

    def constraint(self, name: str) -> DDL:
        return self._constraints.get(name, DDL.empty())


class Schema(DDL):

    def __init__(self, name: str, ddl: str) -> None:
        super().__init__(name=name, schema=name, ddl=ddl)
        self._schema_box: SchemaBox = SchemaBox()

    @property
    def get(self) -> SchemaBox:
        return self._schema_box

    def file_name(self) -> str:
        return f"{self.name}.sql"

    def drop(self) -> str:
        return self.drop_if_exists()

    def drop_if_exists(self) -> str:
        return f"DROP SCHEMA IF EXISTS {self.schema};"

    def drop_cascade(self) -> str:
        return f"DROP SCHEMA IF EXISTS {self.schema} CASCADE;"

    def create_external(self, prefix: str) -> str:
        return f"CREATE EXTERNAL SCHEMA {prefix}_{self.schema};"

    def set_schema_box(self, schema_box: SchemaBox):
        self._schema_box = schema_box

    def items(self) -> List[DDL]:
        return self._schema_box.ddl()

    def map_constraints(self) -> None:
        for table in self._schema_box.tables().values():
            for constraint in self._schema_box.constraints().values():
                if constraint.table == table.name:
                    table.add_constraint(constraint)
