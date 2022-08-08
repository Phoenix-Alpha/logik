import random
from typing import List

from faker.providers import BaseProvider

from ...common_factories import fake as fake  # explicit reexport
from .graphql_types import Function


class FunctionManagerProvider(BaseProvider):
    def function(self) -> Function:
        return Function(name=fake.microservice())

    def functions(self) -> List[Function]:
        return [fake.function() for _ in range(random.randrange(1, 5))]


fake.add_provider(FunctionManagerProvider)
