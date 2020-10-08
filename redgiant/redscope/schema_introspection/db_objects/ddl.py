from abc import ABC, abstractmethod


class DDL(ABC):

    def __init__(self, name: str, schema: str = None):
        self.name = name
        self.schema = schema

    @abstractmethod
    def file_name(self) -> str:
        pass

    @abstractmethod
    def create(self) -> str:
        pass

    @abstractmethod
    def create_if_not_exist(self) -> str:
        pass

    @abstractmethod
    def drop(self) -> str:
        pass

    @abstractmethod
    def drop_if_exist(self) -> str:
        pass
