from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Json


class FieldType(str, Enum):
    STRING = "str"
    INTEGER = "int"
    BOOLEAN = "bool"
    FLOAT = "float"
    DATE = "date"
    DATETIME = "datetime"
    JSON = "json"
    REFERENCE = "reference"

    # ARRAY ?


class FieldModel(BaseModel):
    id: str
    name: str
    type: FieldType
    reference_table_id: Optional[str]
    required: bool = False
    localized: bool = False


class TableModel(BaseModel):
    id: str
    name: str
    display_field: str
    description: Optional[str]
    fields: List[FieldModel]


class ItemModel(BaseModel):
    id: str
    table: TableModel
    values: Json
