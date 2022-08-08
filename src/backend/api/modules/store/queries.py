from typing import List

import strawberry

from ...permissions import IsAuthenticated
from .factories import fake
from .graphql_types import Module


@strawberry.type
class StoreQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def module(self) -> Module:
        module: Module = fake.module()
        return module

    @strawberry.field(permission_classes=[IsAuthenticated])
    def modules(self) -> List[Module]:
        return fake.modules()  # type: ignore
