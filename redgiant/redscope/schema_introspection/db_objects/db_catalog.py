from typing import List, Dict
from redgiant.redscope.schema_introspection.db_objects.ddl import DDL
from redgiant.redscope.schema_introspection.db_objects.schema import Schema
from redgiant.redscope.schema_introspection.db_objects.group import Group
from redgiant.redscope.schema_introspection.db_objects.view import View
from redgiant.redscope.schema_introspection.db_objects.table import Table
from redgiant.redscope.schema_introspection.db_objects.user import User
from redgiant.redscope.schema_introspection.db_objects.constraint import Constraint
from redgiant.redscope.schema_introspection.db_objects.usergroup import UserGroup
from redgiant.redscope.schema_introspection.db_objects.udf import UDF
from redgiant.redscope.schema_introspection.db_objects.ownership import Ownership


# TODO: review this approach, object could be simple dictionary?
class DbCatalog:

    def __init__(self,
                 schemas: List[Schema] = None,
                 groups: List[Group] = None,
                 views: List[View] = None,
                 tables: List[Table] = None,
                 users: List[User] = None,
                 constraints: List[Constraint] = None,
                 membership: List[UserGroup] = None,
                 udfs: List[UDF] = None,
                 ownership: List[Ownership] = None):

        self._schemas = schemas or {}
        self._groups = groups or {}
        self._views = views or {}
        self._tables = tables or {}
        self._users = users or {}
        self._constraints = constraints or {}
        self._membership = membership or {}
        self._udfs = udfs or {}
        self._ownership = ownership or {}

        self._schemas = {schema.name: schema for schema in self._schemas}
        self._groups = {group.name: group for group in self._groups}
        self._views = {view.name: view for view in self._views}
        self._tables = {table.full_name: table for table in self._tables}
        self._users = {user.name: user for user in self._users}
        self._constraints = {constraint.name: constraint for constraint in self._constraints}
        self._membership = {member.name: member for member in self._membership}
        self._udfs = {udf.name: udf for udf in self._udfs}
        self._ownership = {(f"{o.schema}" if o.db_obj_type == 'schema' else f"{o.schema}.{o.name}"): o for o in self._ownership}

    @property
    def schemas(self) -> List[Schema]:
        return [schema for schema in self._schemas.values()]

    @property
    def groups(self) -> List[Schema]:
        return [group for group in self._groups.values()]

    @property
    def views(self) -> List[View]:
        return [view for view in self._views.values()]

    @property
    def tables(self) -> List[Table]:
        return [table for table in self._tables.values()]

    @property
    def users(self) -> List[User]:
        return [user for user in self._users.values()]

    @property
    def constraints(self) -> List[Constraint]:
        return [constraint for constraint in self._constraints.values()]

    @property
    def membership(self) -> List[UserGroup]:
        return [member for member in self._membership.values()]

    @property
    def udfs(self) -> List[UDF]:
        return [udf for udf in self._udfs.values()]

    @property
    def ownership(self) -> List[Ownership]:
        return [ownership for ownership in self._ownership.values()]

    @property
    def file_object_names(self) -> List[str]:
        return ['tables', 'schemas', 'views', 'groups', 'membership', 'users', 'udfs', 'ownership']

    def get_db_objects(self, db_obj_type: str) -> List[DDL]:
        ddl_objs = getattr(self, f"_{db_obj_type}")
        return [ddl for ddl in ddl_objs.values()]

    def get_schema(self, name: str) -> Schema:
        return self._schemas[name]

    def get_group(self, name: str) -> Group:
        return self._groups[name]

    def get_view(self, name: str) -> View:
        return self._views[name]

    def get_table(self, name: str) -> Table:
        return self._tables[name]

    def get_user(self, name: str) -> User:
        return self._users[name]

    def get_constraint(self, name: str) -> Constraint:
        return self._constraints[name]

    def get_user_group(self, name: str) -> UserGroup:
        return self._usergroups[name]

    def get_tables_by_schema(self, schema: str) -> Dict[str, Table]:
        return {table.full_name: table for table in self.tables if table.schema == schema}

    def get_udf(self, name: str) -> UDF:
        return self._udfs[name]

    def get_ownership(self, name: str) -> Ownership:
        return self._ownership[name]

    def get_objects_by_schema(self, schema_name: str) -> Dict:
        db_objs = {}
        db_obj_names = ['tables', 'views', 'udfs']

        schema = self.get_schema(schema_name)
        db_objs[schema.name] = {}

        for db_obj_name in db_obj_names:
            db_objs[schema.name][db_obj_name] = []
            for dbo in getattr(self, f"_{db_obj_name}").values():
                if dbo.schema == schema.name:
                    db_objs[schema.name][db_obj_name].append(dbo)

        return db_objs
