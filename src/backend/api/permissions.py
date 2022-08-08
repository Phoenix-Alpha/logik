from typing import Any

import jwt
from strawberry.permission import BasePermission
from strawberry.types import Info

from . import settings


class IsAuthenticated(BasePermission):
    message = "Valid authorization token not provided"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:  # type: ignore
        authorization = info.context["request"].headers.get("authorization", "")

        if "Bearer " not in authorization:
            return False

        token = authorization.split("Bearer ")[-1]

        jwt.decode(jwt=token, key=settings.JWT_SECRET, algorithms=["HS256"])
        return True


class IsSuperAdmin(BasePermission):
    message = "Invalid API key"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:  # type: ignore
        api_key = info.context["request"].headers.get("x-api-key")
        return bool(api_key == settings.SUPERADMIN_API_KEY)


# TODO: define this permission
class IsWorkspaceOwner(BasePermission):
    pass
