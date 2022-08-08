import random
from typing import List

import strawberry

from ...permissions import IsAuthenticated
from .graphql_types import Flow
from .providers import fake


@strawberry.type
class FlowManagerQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def flow(self, flow_id: int) -> Flow:
        flow: Flow = fake.flow()
        return flow

    @strawberry.field(permission_classes=[IsAuthenticated])
    def flows(self) -> List[Flow]:
        return [fake.flow() for _ in range(random.randint(1, 5))]
