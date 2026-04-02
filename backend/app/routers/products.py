import csv
import io
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user_id, get_current_user_role, require_admin
from app.models.user import UserRole
from app.schemas.product import (
    ProductCreate,
    ProductFilterParams,
    ProductListResponse,
    ProductOut,
    ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductListResponse)
async def list_products(
    search: str | None = Query(None, description="Full-text search by name or SKU"),
    tag_ids: Annotated[list[int], Query()] = [],
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    _: int = Depends(get_current_user_id),
) -> ProductListResponse:
    params = ProductFilterParams(search=search, tag_ids=tag_ids, skip=skip, limit=limit)
    svc = ProductService(db)
    total, products = await svc.list_products(params)
    return ProductListResponse(
        total=total,
        items=[ProductOut.model_validate(p) for p in products],
    )


@router.get("/export", dependencies=[Depends(require_admin)])
async def export_products_csv(
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """Export all products as CSV (admin only)."""
    params = ProductFilterParams(skip=0, limit=10_000)
    svc = ProductService(db)
    _, products = await svc.list_products(params)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "SKU", "Description", "Quantity", "Price", "Last Received", "Tags"])
    for p in products:
        writer.writerow([
            p.id, p.name, p.sku, p.description or "",
            p.quantity, float(p.price),
            p.last_received_at.isoformat() if p.last_received_at else "",
            "|".join(t.name for t in p.tags),
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products_export.csv"},
    )


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    _: int = Depends(get_current_user_id),
) -> ProductOut:
    svc = ProductService(db)
    product = await svc.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut.model_validate(product)


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    _: int = Depends(get_current_user_id),
) -> ProductOut:
    svc = ProductService(db)
    if await svc.get_by_sku(data.sku):
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")
    product = await svc.create_product(data)
    return ProductOut.model_validate(product)


@router.patch("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    role: UserRole = Depends(get_current_user_role),
) -> ProductOut:
    svc = ProductService(db)
    product = await svc.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = await svc.update_product(product, data)
    return ProductOut.model_validate(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)) -> None:
    svc = ProductService(db)
    product = await svc.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await svc.delete_product(product)
