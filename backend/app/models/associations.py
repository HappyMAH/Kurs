from sqlalchemy import Column, ForeignKey, Integer, Table

from app.core.database import Base

# Many-to-many association table: products <-> tags
product_tags = Table(
    "product_tags",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
