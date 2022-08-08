import typing

import strawberry

from ...permissions import IsAuthenticated
from .factories import fake
from .graphql_types import Function


@strawberry.type
class FunctionManagerQuery:
    function: Function = strawberry.field(
        resolver=fake.function, permission_classes=[IsAuthenticated]
    )
    functions: typing.List[Function] = strawberry.field(
        resolver=fake.functions, permission_classes=[IsAuthenticated]
    )
