from itertools import groupby
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


"""
Catalog Model

schema
    tables
        constraints
    views
    functions
    procedures
    
"""

# TODO: review this approach, object could be simple dictionary?


class RedshiftSchema:

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

        self.ddl = {
            'schemas': {schema.name: schema for schema in schemas},
            'groups': {group.name: group for group in groups},
            'users': {user.name: user for user in users},
            'membership': {member.name: member for member in membership},
            'ownership': {(f"{o.schema}" if o.db_obj_type == 'schema' else f"{o.schema}.{o.name}"): o for o in ownership}
        }

        """
        use group by here to group objects below
        
        eg.
        tables by schema
        
        for each schema in tables by schema
            get the schema
                add the tables
            
        """
        groupings = {'tables': tables, 'views': views, 'udfs': udfs}
        mapping = {}

        for name, ddls in groupings.items():
            group = {}
            ddls.sort(key=lambda x: x.schema)

            for key, group in groupby(ddls, lambda x: x.schema):
                group[key] = group

            mapping[name] = group

        self.mapping = mapping
