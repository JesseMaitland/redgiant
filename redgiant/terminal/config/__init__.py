import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from configparser import ConfigParser
from psycopg2.extensions import connection


class RedGiantConfig:

    def __init__(self) -> None:

        config_path = Path.cwd() / ".redgiant"

        self.config = ConfigParser()
        self.config.read(config_path)

        env_file_path = Path.cwd() / self.config.get('environment', 'env_file')
        load_dotenv(env_file_path)

    def get_s3_bucket(self, name: str) -> str:
        value = self.config.get('s3_buckets', name)
        return os.environ.get(value, value)

    def get_iam_role(self, name: str) -> str:
        value = self.config.get('iam_roles', name)
        return os.environ.get(value, value)

    def get_db_connection(self, name: str) -> connection:
        value = self.config.get('database', name)
        connection_string = os.environ.get(value, value)
        return psycopg2.connect(connection_string)

    def get_project_root(self) -> str:
        return self.config.get('project', 'root')
