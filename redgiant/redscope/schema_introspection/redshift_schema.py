from itertools import groupby
from typing import List, Dict
from redgiant.redscope.schema_introspection.db_objects.ddl import DDL
from redgiant.redscope.schema_introspection.db_objects.schema import Schema, SchemaBox
from redgiant.redscope.schema_introspection.db_objects.group import Group
from redgiant.redscope.schema_introspection.db_objects.view import View
from redgiant.redscope.schema_introspection.db_objects.table import Table
from redgiant.redscope.schema_introspection.db_objects.user import User
from redgiant.redscope.schema_introspection.db_objects.constraint import Constraint
from redgiant.redscope.schema_introspection.db_objects.usergroup import UserGroup
from redgiant.redscope.schema_introspection.db_objects.udf import UDF
from redgiant.redscope.schema_introspection.db_objects.ownership import Ownership


class RedshiftSchema:
    # 'groups', 'users', 'membership', 'ownership'
    allowed_kwargs = ['schemas']
    allowed_mappings = ['tables', 'views', 'udfs', 'procedures', 'constraints']

    def __init__(self, **kwargs):

        self._validate_kwargs(self.allowed_kwargs, kwargs)

        for kwarg in self.allowed_kwargs:
            setattr(self, f"_{kwarg}", kwargs.get(kwarg, {}))

        self.schema_mapping = {}

    def schemas(self):
        return getattr(self, '_schemas')

    def schema(self, name: str) -> Schema:
        return self.schemas()[name]

    @staticmethod
    def _validate_kwargs(allowed_kwargs: List[str], kwargs):
        for kwarg in kwargs.keys():
            if kwarg not in allowed_kwargs:
                raise ValueError(f"redshift schema got unexpected keyword {kwarg}")

    def map_schemas(self, **kwargs):
        self._validate_kwargs(self.allowed_mappings, kwargs)

        mapping = {}
        for name, ddls in kwargs.items():  # eg. tables:{table_name: ddl object}

            schema_grouping = {}
            ddls.sort(key=lambda x: x.schema)

            for schema, group in groupby(ddls, lambda x: x.schema):
                schema_grouping[schema] = list(group)

            mapping[name] = schema_grouping

        for schema_name, schema in self.schemas().items():
            schema_mapping = {}  # add the schema to the mapping

            for db_object_type, ddls in mapping.items():
                items = ddls.get(schema_name, None)

                if items:
                    schema_mapping[db_object_type] = items

            schema_box = SchemaBox(**schema_mapping)
            schema.set_schema_box(schema_box)
            schema.map_constraints()
