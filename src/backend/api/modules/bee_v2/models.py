from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Barcode(BaseModel):
    id: int
    account_id: int
    company_id: int
    article_id: int
    name: str
    supplier_name: Optional[str] = None
    supplier_article_code: Optional[str] = None
    quantity: Optional[float]
    rotation: str
    preparation_mode: int
    flag_double: int
    created: Optional[datetime] = Field(default_factory=datetime.now)
    created_by: Optional[str]
    modified: Optional[datetime] = Field(default_factory=datetime.now)
    modified_by: Optional[str]


class Article(BaseModel):
    id: int
    account_id: int
    company_id: int
    status: int
    code: str
    name: str
    additional_description: Optional[str] = None
    supplier_name: Optional[str] = None
    length: float = Field(description="Length in centimeters (cm)")
    width: float = Field(description="Width in centimeters (cm)")
    height: float = Field(description="Height in centimeters (cm)")
    base_unit_price: Optional[float]
    base_unit_weight: float = Field(description="Weight in kilograms (kg)")
    box_weight: float
    box_quantity: float
    base_unit_picking: bool
    box_picking: bool
    base_unit_rotation: Optional[str] = None
    box_rotation: Optional[str] = None
    cubing_type: int
    feature_type_id: Optional[int]
    permanent_product: bool
    tariff_classification: Optional[str] = None
    family: Optional[str] = None
    subfamily: Optional[str] = None
    grouping_id: Optional[str] = None
    created: Optional[datetime] = Field(default_factory=datetime.now)
    created_by: Optional[str]
    modified: Optional[datetime] = Field(default_factory=datetime.now)
    modified_by: Optional[str]

    # References
    barcodes: List[Barcode]
