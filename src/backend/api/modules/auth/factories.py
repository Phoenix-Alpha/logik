import random
from typing import List

from faker.providers import BaseProvider
from slugify import slugify

from ...common_factories import fake as fake  # explicit reexport
from .graphql_types import UserType, WorkspaceType
from .models import Role


class AuthProvider(BaseProvider):
    def user(self) -> UserType:
        return UserType(
            username=fake.username(),
            email=fake.email(),
            is_active=fake.pybool(),
            role=Role.READ,
            workspace_ids=["a", "b"],
        )

    def users(self) -> List[UserType]:
        return [self.user() for _ in range(random.randint(0, 5))]

    def api_key(self) -> str:
        API_KEY_PREFIX = "lgk"
        API_KEY_LENGTH = 12
        return "_".join(
            [
                API_KEY_PREFIX,
                fake.pystr(min_chars=API_KEY_LENGTH, max_chars=API_KEY_LENGTH),
            ]
        )

    def workspace(self) -> WorkspaceType:
        company = fake.company()
        environment = random.choice(["dev", "prod", "staging", "test", "qa"])
        name = f"{company}-{environment}"
        return WorkspaceType(
            id=fake.pystr(min_chars=10, max_chars=10),
            name=name,
            slug=slugify(name),
        )

    def workspaces(self) -> List[WorkspaceType]:
        return [self.workspace() for _ in range(random.randint(1, 5))]


fake.add_provider(AuthProvider)
