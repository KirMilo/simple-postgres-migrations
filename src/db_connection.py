from abc import ABC

from psycopg import Connection, connect


class DB(ABC):
    host: str
    port: int
    user: str
    password: str
    dbname: str

    def __init__(self):
        self.dsn = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        self.__connection: Connection | None = None

    @property
    def conn(self) -> Connection:
        if self.__connection is None:
            self.__connection = connect(self.dsn)
        return self.__connection


class TargetDB(DB):
    host = "host"
    port = 5432
    user = "user"
    password = "password"
    dbname = "db1"


class MainDB(DB):
    host = "host"
    port = 5432
    user = "user"
    password = "password"
    dbname = "db2"
