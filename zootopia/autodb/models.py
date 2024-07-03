from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel

from zootopia.langchain.models import LLMConfig


class TableType(Enum):
    ROW = "row"
    COL = "column"


class DataType(Enum):
    LIST = "list"
    JSON = "json"
    DICT = "json"
    BOOL = "boolean"
    STR = "string"
    INT = "integer"
    TIMESTAMP = "timestamp"


class DatabaseColumn(BaseModel):
    name: str
    datatype: DataType
    description: str


class DatabaseTable(BaseModel):
    name: str
    table_type: TableType
    description: str
    llm_control: bool
    columns: list[DatabaseColumn]


class AutoDBConfig(BaseModel):
    database_tables: list[DatabaseTable]
    intent_llm_config: LLMConfig


class DataLocation(BaseModel):
    table: str
    column: Optional[str]


class DataAction(BaseModel):
    data_location: DataLocation
    data: dict
