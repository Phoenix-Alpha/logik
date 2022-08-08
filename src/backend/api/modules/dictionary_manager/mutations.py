from typing import List, Optional

import strawberry

from ...common_factories import fake
from .models import FieldModel, FieldType, TableModel


@strawberry.input
class FieldModelInput:
    name: str
    type: FieldType
    reference_table_id: Optional[str] = None
    required: bool = False
    localized: bool = False


@strawberry.input
class CreateTableInput:
    name: str
    display_field: str
    fields: List[FieldModelInput]
    description: Optional[str] = None

    def to_model(self) -> TableModel:
        fields = [
            FieldModel(
                id=fake.uuid4(),
                name=field.name,
                type=field.type,
                reference_table_id=field.reference_table_id,
                required=field.required,
                localized=field.localized,
            )
            for field in self.fields
        ]

        # assume each table requires `id` column
        id = next(filter(lambda f: f.name == "id", fields), None)
        if not id:
            fields.insert(
                0,
                FieldModel(
                    id=fake.uuid4(),
                    name="id",
                    type=FieldType.STRING,
                ),
            )

        return TableModel(
            id=fake.uuid4(),
            name=self.name,
            description=self.description,
            display_field=self.display_field,
            fields=fields,
        )


# @strawberry.type
# class DictionaryManagerMutation:
#     @strawberry.mutation
#     def create_table(self, input: CreateTableInput) -> Table:
#         model = input.to_model()
#         # Create table in DB ?
#         return Table.from_pydantic(model)
