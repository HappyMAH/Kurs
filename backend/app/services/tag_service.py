from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


class TagService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, tag_id: int) -> Tag | None:
        result = await self.db.execute(select(Tag).where(Tag.id == tag_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Tag | None:
        result = await self.db.execute(select(Tag).where(Tag.name == name))
        return result.scalar_one_or_none()

    async def list_tags(self) -> list[Tag]:
        result = await self.db.execute(select(Tag).order_by(Tag.name))
        return list(result.scalars().all())

    async def get_many_by_ids(self, tag_ids: list[int]) -> list[Tag]:
        if not tag_ids:
            return []
        result = await self.db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
        return list(result.scalars().all())

    async def create_tag(self, data: TagCreate) -> Tag:
        tag = Tag(name=data.name, color=data.color)
        self.db.add(tag)
        await self.db.flush()
        await self.db.refresh(tag)
        return tag

    async def update_tag(self, tag: Tag, data: TagUpdate) -> Tag:
        update_data = data.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(tag, field, value)
        await self.db.flush()
        await self.db.refresh(tag)
        return tag

    async def delete_tag(self, tag: Tag) -> None:
        await self.db.delete(tag)
        await self.db.flush()
