from typing import Optional

import strawberry

from .factories import fake
from .models import Permission, Role
from .models import User as UserModel


@strawberry.type
class LoginSuccess:
    access_token: str = strawberry.field(
        description=(
            "A short-lived JWT that can be used to authenticate a user onto the"
            " platform"
        )
    )
    # refresh_token: str = strawberry.field(
    #     "A long-lasting JWT dedicated to refreshing auth tokens"
    # )


# Declare the enum as a Strawberry enum
strawberry.enum(Role, name="Role")


@strawberry.experimental.pydantic.type(
    name="Permission", model=Permission, all_fields=True
)
class PermissionType:
    pass


# FIXME: we cannot use the `pydantic.experimental` decorator here because
# it doesn't support the ForwardRef on `owner`. Hopefully they'll fix this in
# a later version of Strawberry
@strawberry.type(name="Workspace")
class WorkspaceType:
    name: str
    slug: str
    owner: "Optional[UserType]" = None
    id: str = strawberry.field(
        description=(
            "This is your workspace's auto-generated unique identifier. "
            "It can't be changed."
        ),
        default_factory=fake.id,
    )


@strawberry.experimental.pydantic.type(name="User", model=UserModel)
class UserType:
    username: strawberry.auto
    email: strawberry.auto
    workspace: WorkspaceType
    permissions: strawberry.auto
    created_at: strawberry.auto

    # @strawberry.field
    # def full_name(self) -> str:
    #     return f"{self.first_name} {self.last_name}"
