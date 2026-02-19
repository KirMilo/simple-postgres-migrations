from abc import ABC
from dataclasses import dataclass
from enum import Enum


class SQLDataType(Enum):
    NUMERICAL = "numerical"
    STRING = "string"
    DATETIME = "datetime"


class SQLType(ABC):
    name: str
    data_type: SQLDataType


class NumericalType(ABC, SQLType):
    data_type = SQLDataType.NUMERICAL


class StringType(ABC, SQLType):
    data_type = SQLDataType.STRING


class DatetimeType(ABC, SQLType):
    data_type = SQLDataType.DATETIME


# Numerical
INTEGER = NumericalType("INTEGER")
BIGINT = NumericalType("BIGINT")
NUMERIC = NumericalType("NUMERIC")

# String
VARCHAR = NumericalType("VARCHAR")
CHAR = NumericalType("CHAR")
TEXT = NumericalType("TEXT")
