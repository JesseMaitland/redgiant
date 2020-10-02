from importlib import import_module
from pathlib import Path
from typing import Tuple, List, Union
from psycopg2.extensions import connection
from redscope.database.models import IntrospectionQueries
from redscope.schema_introspection.formatters.base_formatter import DDLFormatter
from redscope.schema_introspection.db_objects.db_catalog import DbCatalog
from redscope.schema_introspection.db_objects.ddl import DDL


class DbIntrospection:

    allowed_db_objects = ['groups', 'schemas', 'users', 'tables', 'views', 'constraints', 'membership', 'udfs', 'ownership']

    def __init__(self, introspection_queries: IntrospectionQueries, db_object: str = ''):

        self.introspection_queries = introspection_queries
        self.db_object = None
        self.formatter_path = None

        if db_object:
            self.set_introspection_path(db_object)

    def set_introspection_path(self, db_object: str):
        self.validate_db_object(db_object)
        self.db_object = db_object
        self.formatter_path = Path("redscope/schema_introspection/formatters") / db_object
        self.formatter_path = self.formatter_path.as_posix().replace('/', '.')

    def __call__(self, db_object: str) -> List[DDL]:
        self.set_introspection_path(db_object)
        formatter = self._import_formatter()
        raw_ddl = self._execute_query()
        return formatter.format(raw_ddl)

    def _execute_query(self) -> Tuple[str]:
        return self.introspection_queries.call_query(self.db_object)

    def _import_formatter(self) -> DDLFormatter:
        formatter_module = import_module(self.formatter_path)
        formatter = getattr(formatter_module, f"{self.db_object.capitalize().rstrip('s')}Formatter")
        return formatter()

    def validate_db_object(self, db_object: str):
        if db_object not in self.allowed_db_objects:
            raise ValueError(f'{db_object} is not a valid name. Allowed values are {self.allowed_db_objects}')


def introspect_redshift(db_connection: connection, object_type: Union[str, List[str]] = None, verbose: bool = False) -> DbCatalog:
    """
    Function used to introspect redshift database objects
    Args:
        db_connection: psycopg2 connection object to a running instance of redshift.
        object_type: str or list the type of redshift object to introspect
        verbose: When True, will print out the introspection steps to the terminal

    Returns: DbCatalog: This is a dictionary like object which contains the requested ddl

    """
    if object_type is None:
        objects_to_introspect = DbIntrospection.allowed_db_objects.copy()
    else:
        if type(object_type) == str:
            objects_to_introspect = [object_type]
        else:
            objects_to_introspect = object_type

    # we don't want to introspect constraints on their own, just remove the value
    # and if the list is empty afterward, we know they tried to introspect constraints
    # without the context of a corresponding table, which doesn't make sense really.
    try:
        objects_to_introspect.remove('constraints')
    except ValueError:
        pass

    if not objects_to_introspect:
        raise ValueError("constraints are not allowed to be introspected without reference to a table.")

    queries = IntrospectionQueries(db_connection)
    introspect = DbIntrospection(queries)
    introspected_objects = {}

    for object_to_introspect in objects_to_introspect:

        if verbose:
            print(f"Introspecting Redshift ........ {object_to_introspect}")

        db_objects = introspect(object_to_introspect)

        # if we are introspecting tables, look up their corresponding constraints
        # and make the association.
        if object_to_introspect == 'tables':
            constraints = introspect('constraints')

            for table in db_objects:
                for constraint in constraints:
                    if constraint.schema == table.schema and constraint.table == table.name:
                        table.add_constraint(constraint)

        introspected_objects[object_to_introspect] = db_objects

    return DbCatalog(**introspected_objects)
