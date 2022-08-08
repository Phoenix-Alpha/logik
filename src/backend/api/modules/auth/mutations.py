from typing import Optional

import jwt
import strawberry
from slugify import slugify

from ... import settings
from ...permissions import IsAuthenticated, IsSuperAdmin
from .factories import fake
from .graphql_types import LoginSuccess, UserType, WorkspaceType
from .models import User, Workspace

# Mutation


@strawberry.type
class AuthMutation:
    @strawberry.mutation(
        description="Obtain a JSON Web Token (JWT) to use in the frontend"
    )
    def login(
        self, username: str, password: str, workspace_id: strawberry.ID
    ) -> Optional[LoginSuccess]:
        assert password == "$ecret"
        # Create a token
        payload = {
            "workspace_id": workspace_id,
            "username": username,
            "permissions": {"Article": "READ"},
        }
        access_token = jwt.encode(
            payload=payload,
            key=settings.JWT_SECRET,
        )
        return LoginSuccess(access_token=access_token)

    @strawberry.mutation(
        description="Invite a new User via email",
        permission_classes=[IsAuthenticated],
    )
    def invite_user(self, email: str, workspace_id: strawberry.ID, role: str) -> str:
        # Check is workspace owner ?
        return f"TODO: invite {email}"

    @strawberry.mutation(
        description="Create a new Workspace", permission_classes=[IsSuperAdmin]
    )
    def create_workspace(self, name: str, owner_email: str) -> WorkspaceType:
        workspace = Workspace(name=name, slug=slugify(name))
        workspace_type = WorkspaceType(**workspace.dict())
        # Create User
        owner = User(
            username=owner_email,
            email=owner_email,
            password=fake.password(),
            workspace=workspace,
            permissions=[],
        )
        owner_type = UserType.from_pydantic(owner)
        # Assign owner to Workspace
        workspace_type.owner = owner_type
        return workspace_type
