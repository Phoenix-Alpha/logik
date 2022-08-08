import random
from typing import List, Union

import faker

from ...common_factories import fake as fake  # explicit reexport
from .graphql_types import Choice, Edge, Fetch, Flow, Node, Task


class FlowManagerProvider(faker.providers.BaseProvider):
    def fetch(self) -> Fetch:
        return Fetch(entry_id=fake.uuid4())

    def choice(self) -> Choice:
        return Choice(default="foo")

    def task(self) -> Task:
        return Task(function_id=fake.uuid4())

    def node(self) -> Node:
        choices: List[Union[Fetch, Choice, Task]] = [
            self.fetch(),
            self.choice(),
            self.task(),
        ]
        return random.choice(choices)

    def edge(self) -> Edge:
        return Edge(source=fake.node(), target=fake.node())

    def edges(self) -> List[Edge]:
        return [fake.edge() for _ in range(random.randint(1, 5))]

    def flow(self) -> Flow:
        return Flow(
            id=fake.uuid4(),
            name=fake.microservice(),
            description=fake.sentence(),
            edges=self.edges(),
        )

    def flows(self) -> List[Flow]:
        return [self.flow() for _ in range(random.randint(1, 5))]


fake.add_provider(FlowManagerProvider)
