from app.core.database import Base  # noqa: F401 – imported so Alembic sees all models
from app.models.user import User  # noqa: F401
from app.models.product import Product  # noqa: F401
from app.models.tag import Tag  # noqa: F401
from app.models.associations import product_tags  # noqa: F401
