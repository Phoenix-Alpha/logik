import strawberry

from ..modules.auth.mutations import AuthMutation
from ..modules.bee_v2.mutations import Beev2Mutation
from ..modules.bee_v2.queries import Beev2Query


@strawberry.type
class Query(Beev2Query):
    pass


@strawberry.type
class Mutation(
    AuthMutation,
    Beev2Mutation,
):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
