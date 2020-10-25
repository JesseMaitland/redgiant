from redgiant.redscope.introspection.ddl import DDL


class Ownership(DDL):

    def __init__(self, schema: str, name: str, owner: str, signature: str, db_obj_type: str):
        self.schema = schema
        self.db_obj_type = db_obj_type
        self.owner = owner
        self.signature = signature
        super().__init__(name)

    @property
    def file_name(self) -> str:

        if self.db_obj_type == 'schema':
            return f"{self.schema}.sql"

        else:
            return f"{self.name}.sql"

    @property
    def create(self) -> str:

        # TODO: This is really ugly....
        if self.db_obj_type in ['function', 'procedure']:
            n = f"{self.db_obj_type.upper()}"
            o = f"{self.schema}.{self.name}{self.signature}"

        elif self.db_obj_type == 'schema':
            n = f"{self.db_obj_type.upper()}"
            o = f"{self.schema}"

        elif self.db_obj_type == 'view':
            n = "TABLE"
            o = f"{self.schema}.{self.name}"

        else:
            n = f"{self.db_obj_type.upper()}"
            o = f"{self.schema}.{self.name}"

        return f"ALTER {n} {o} OWNER TO {self.owner}"

    @property
    def create_if_not_exist(self) -> str:
        return self.create

    @property
    def drop(self) -> str:
        raise NotImplementedError

    @property
    def drop_if_exist(self) -> str:
        raise NotImplementedError

    @property
    def drop_if_exists_cascade(self) -> str:
        raise NotImplementedError
