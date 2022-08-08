from typing import List, Optional

from pydantic import BaseModel


class Module(BaseModel):
    id: str
    name: str
    description: str
    version: str
    author: str
    screenshots: Optional[List[str]]
    depends_on: List["Module"]
    rating: float
    num_installs: int
    graphql_schema: Optional[str]
    # widgets: Optional[List[Widget]]
    # documents
    # flows
    # tables
    price = float
