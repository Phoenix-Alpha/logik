import strawberry

from ...permissions import IsAuthenticated, IsWorkspaceOwner
from .factories import fake


@strawberry.type
class Beev2Mutation:
    @strawberry.mutation(
        description="Reset a user's password",
        permission_classes=[IsAuthenticated, IsWorkspaceOwner],
    )
    def reset_user(self, username: str) -> str:
        password: str = fake.password()
        return password
