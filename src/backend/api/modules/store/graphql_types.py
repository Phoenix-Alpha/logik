import strawberry

from .models import Module as ModuleModel

# @strawberry.type
# class Review:
#     rating: int
#     comment: Optional[str]


@strawberry.experimental.pydantic.type(model=ModuleModel)
class Module:
    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    version: strawberry.auto
    author: strawberry.auto
    screenshots: strawberry.auto
    rating: strawberry.auto = strawberry.field(
        description="Average rating of the Module"
    )
    num_installs: strawberry.auto = strawberry.field(
        description="Number of times the Module was installed into a Workspace"
    )
    graphql_schema: strawberry.auto
    price = strawberry.auto


# @strawberry.type(description="A module that is depended on by another module")
# class ModuleDependency:
#     module: Module
#     version: str
