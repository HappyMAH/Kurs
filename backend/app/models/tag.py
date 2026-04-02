from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.associations import product_tags


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    color: Mapped[str] = mapped_column(String(7), default="#6366f1", nullable=False)  # hex color

    products: Mapped[list["Product"]] = relationship(  # type: ignore[name-defined]
        "Product", secondary=product_tags, back_populates="tags", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Tag id={self.id} name={self.name!r}>"
