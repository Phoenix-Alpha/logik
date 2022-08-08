from typing import List, Optional

import strawberry


@strawberry.type
class Choice:
    default: str


@strawberry.type
class Task:
    function_id: strawberry.ID


@strawberry.type(description="Get an Entry by its ID")
class Fetch:
    entry_id: strawberry.ID


Node = strawberry.union(
    name="Node",
    types=(Choice, Task, Fetch),
    description="A Node is a state that can be orchestrated in a Flow",
)


@strawberry.type
class Edge:
    source: Node
    target: Node


@strawberry.type
class Flow:
    id: strawberry.ID
    name: str
    description: Optional[str]
    edges: List[Edge]
