from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.associations import product_tags
from app.models.product import Product
from app.models.tag import Tag
from app.schemas.product import ProductCreate, ProductFilterParams, ProductUpdate
from app.services.tag_service import TagService


class ProductService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self._tag_svc = TagService(db)

    # ── Internal helpers ────────────────────────────────────────────────────

    def _base_query(self):
        return select(Product)

    def _apply_search(self, query, search: str):
        term = f"%{search}%"
        return query.where(
            or_(
                Product.name.ilike(term),
                Product.sku.ilike(term),
            )
        )

    def _apply_tag_filter(self, query, tag_ids: list[int]):
        """
        AND-intersection: return products that have ALL given tags.
        Uses a sub-query counting matching rows in product_tags.
        """
        for tag_id in tag_ids:
            subq = (
                select(product_tags.c.product_id)
                .where(product_tags.c.tag_id == tag_id)
                .scalar_subquery()
            )
            query = query.where(Product.id.in_(subq))
        return query

    # ── Public API ───────────────────────────────────────────────────────────

    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.db.execute(
            self._base_query().where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_by_sku(self, sku: str) -> Product | None:
        result = await self.db.execute(select(Product).where(Product.sku == sku))
        return result.scalar_one_or_none()

    async def list_products(self, params: ProductFilterParams) -> tuple[int, list[Product]]:
        query = self._base_query()

        if params.search:
            query = self._apply_search(query, params.search)

        if params.tag_ids:
            query = self._apply_tag_filter(query, params.tag_ids)

        # Count total before pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        # Apply pagination
        query = query.offset(params.skip).limit(params.limit).order_by(Product.created_at.desc())
        result = await self.db.execute(query)
        products = list(result.scalars().all())

        return total, products

    async def create_product(self, data: ProductCreate) -> Product:
        tags = await self._tag_svc.get_many_by_ids(data.tag_ids)
        product = Product(
            name=data.name,
            sku=data.sku,
            description=data.description,
            quantity=data.quantity,
            price=data.price,
            last_received_at=data.last_received_at,
            tags=tags,
        )
        self.db.add(product)
        await self.db.flush()
        await self.db.refresh(product)
        return product

    async def update_product(self, product: Product, data: ProductUpdate) -> Product:
        update_data = data.model_dump(exclude_none=True, exclude={"tag_ids"})
        for field, value in update_data.items():
            setattr(product, field, value)

        if data.tag_ids is not None:
            product.tags = await self._tag_svc.get_many_by_ids(data.tag_ids)

        await self.db.flush()
        await self.db.refresh(product)
        return product

    async def delete_product(self, product: Product) -> None:
        await self.db.delete(product)
        await self.db.flush()
