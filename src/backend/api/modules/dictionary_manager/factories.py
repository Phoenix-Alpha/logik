import random
from typing import List

from faker.providers import BaseProvider

from ...common_factories import fake as fake  # explicit reexport
from .graphql_types import Field, Item, Table
from .models import FieldType


class DictionaryManagerProvider(BaseProvider):
    def field(self) -> Field:
        field_type = random.choice(list(FieldType))
        if field_type == FieldType.REFERENCE:
            name = fake.word() + "_id"
        else:
            name = fake.word(
                ext_word_list=[
                    "id",
                    "name",
                    "description",
                    "weight",
                    "length",
                    "height",
                    "depth",
                    "version",
                    "status",
                    "patati",
                    "patata",
                ]
            )
        return Field(
            id=fake.id(),
            name=name,
            type=field_type,
            reference_table_id=fake.id() if field_type == FieldType.REFERENCE else None,
        )

    def fields(self) -> List[Field]:
        fields = [self.field() for _ in range(random.randrange(1, 5))]
        # Avoid duplicate field names during generation
        unique_fields = {c.name: c for c in fields}
        return list(unique_fields.values())

    def table(self) -> Table:
        fields = self.fields()
        return Table(
            id=fake.id(),
            name=fake.word(
                ext_word_list=[
                    "article",
                    "parcel",
                    "block",
                    "location",
                    "history",
                    "content",
                    "stock",
                ]
            ),
            description=fake.sentence(),
            display_field=random.choice(fields).name,
            fields=fields,
        )

    def item(self) -> Item:
        """Returns a random Item object"""
        table = self.table()

        faker_mapping = {
            FieldType.STRING: fake.word(),
            FieldType.INTEGER: fake.pyint(),
            FieldType.BOOLEAN: fake.pybool(),
            FieldType.FLOAT: fake.pyfloat(positive=True),
            FieldType.DATE: fake.date(),
            FieldType.DATETIME: fake.date_time().isoformat(),
            FieldType.JSON: fake.json(num_rows=1),
            FieldType.REFERENCE: fake.id(),
        }

        return Item(
            id=fake.id(),
            table=table,
            values={field.name: faker_mapping[field.type] for field in table.fields},
        )

    def generate_items(self) -> List[Item]:
        """Note: we're not using the name `items` to avoid conflicting with Faker's
        native `items` method"""
        return [self.item() for _ in range(random.randrange(1, 5))]


fake.add_provider(DictionaryManagerProvider)
