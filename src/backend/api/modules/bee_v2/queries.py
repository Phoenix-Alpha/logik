import math
from typing import List, Optional

import strawberry

from ...permissions import IsAuthenticated
from .factories import fake
from .graphql_types import Article


@strawberry.input(description="Facets that you can filter on during an Article search")
class FacetFilters:
    id: Optional[str]
    account_id: Optional[str]
    company_id: Optional[str]
    status: Optional[str]
    code: Optional[str]
    name: Optional[str]
    additional_description: Optional[str]
    supplier_name: Optional[str]
    length: Optional[str]
    width: Optional[str]
    height: Optional[str]
    base_unit_price: Optional[str]
    base_unit_weight: Optional[str]
    box_weight: Optional[str]
    box_quantity: Optional[str]
    base_unit_picking: Optional[str]
    box_picking: Optional[str]
    base_unit_rotation: Optional[str]
    box_rotation: Optional[str]
    cubing_type: Optional[str]
    feature_type_id: Optional[str]
    permanent_product: Optional[str]
    tariff_classification: Optional[str]
    family: Optional[str]
    subfamily: Optional[str]
    grouping_id: Optional[str]
    created: Optional[str]
    created_by: Optional[str]
    modified: Optional[str]
    modified_by: Optional[str]


@strawberry.type
class SearchResult:
    results: List[Article]
    count: int
    items_per_page: int
    total_pages: int


@strawberry.type
class Beev2Query:
    @strawberry.field(
        description="Retrieve a given Article by its SKU",
        permission_classes=[IsAuthenticated],
    )
    def article(self, id: strawberry.ID) -> Article:
        return fake.article()

    @strawberry.field(
        description="List multiple articles",
        permission_classes=[IsAuthenticated],
    )
    def articles(
        self,
        filters: Optional[FacetFilters] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 25,
    ) -> SearchResult:
        num_items = fake.pyint(max_value=200)
        results = fake.articles(max_items=num_items)
        count = len(results)
        total_pages = math.ceil(count / items_per_page)
        return SearchResult(
            results=results,
            count=count,
            items_per_page=items_per_page,
            total_pages=total_pages,
        )
