from typing import List

import strawberry
from scalars import JSONScalar

from ... import settings
from ...permissions import IsAuthenticated
from .factories import fake
from .graphql_types import Item


@strawberry.type
class DictionaryManagerQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def item(self, id: str) -> Item:
        if settings.DEBUG:
            item: Item = fake.item()
        else:
            pass
            # response = item_table.get_item(Key={"id": id})
            # item = Item(**response["Item"])
        return item

    @strawberry.field(permission_classes=[IsAuthenticated])
    def items(self, table_name: str, filters: JSONScalar) -> List[Item]:
        f"""
        SELECT *
        FROM {table_name}
        WHERE {filters.x} = y
        """
        return fake.generate_items()  # type: ignore
