from datetime import datetime
from decimal import Decimal

from annotated_types import Ge
from pydantic import BaseModel, Field
from typing import Annotated

from app.schemas.tag import TagOut

# Дополнительный тип для цены: Decimal >= 0
PositiveDecimal = Annotated[Decimal, Ge(0)]


# ── Request schemas ──────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    quantity: int = Field(default=0, ge=0)
    price: PositiveDecimal
    last_received_at: datetime | None = None
    tag_ids: list[int] = Field(default_factory=list)


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    quantity: int | None = Field(None, ge=0)
    price: PositiveDecimal | None = None
    last_received_at: datetime | None = None
    tag_ids: list[int] | None = None


class ProductFilterParams(BaseModel):
    search: str | None = None          # full-text search on name / sku
    tag_ids: list[int] = Field(default_factory=list)  # AND intersection
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=200)


# ── Response schemas ─────────────────────────────────────────────────────────

class ProductOut(BaseModel):
    id: int
    name: str
    sku: str
    description: str | None
    quantity: int
    price: Decimal
    last_received_at: datetime | None
    created_at: datetime
    updated_at: datetime
    tags: list[TagOut] = []

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    total: int
    items: list[ProductOut]
