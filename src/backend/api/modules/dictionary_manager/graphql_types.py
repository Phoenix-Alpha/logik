import strawberry

from ...scalars import JSONScalar
from .models import FieldModel, FieldType, ItemModel, TableModel

FieldTypeEnum = strawberry.enum(FieldType, name="FieldType")


@strawberry.experimental.pydantic.type(model=FieldModel)
class Field:
    id: strawberry.auto
    name: strawberry.auto
    type: FieldTypeEnum
    reference_table_id: strawberry.auto
    required: strawberry.auto
    localized: strawberry.auto


@strawberry.experimental.pydantic.type(model=TableModel, all_fields=True)
class Table:
    pass


@strawberry.experimental.pydantic.type(model=ItemModel)
class Item:
    id: strawberry.auto
    table: strawberry.auto
    values: JSONScalar
