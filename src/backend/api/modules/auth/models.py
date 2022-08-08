from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from .factories import fake


class Role(str, Enum):
    READ = "read"
    WRITE = "write"


class Permission(BaseModel):
    model: str  # FIXME: should be an abstract Type, if that's possible
    role: Role


class Workspace(BaseModel):
    """
    A workspace is a a logical container that isolates resources
    """

    id: str = Field(
        description=(
            "This is your workspace's auto-generated unique identifier. "
            "It can't be changed."
        ),
        default_factory=fake.id,
    )
    name: str = Field(description="Name of the Workspace (e.g. `acme-prod`)")
    slug: str = Field(description="Slug fo the Workspace's name")
    owner: Optional[User] = Field(
        description="User that was assigned as Workspace owner",
        default=None,
    )

    # TODO: calculate slug automatically


class User(BaseModel):
    username: str
    email: Optional[str]
    workspace: Workspace
    permissions: List[Permission]
    created_at: datetime = Field(default_factory=datetime.now)
