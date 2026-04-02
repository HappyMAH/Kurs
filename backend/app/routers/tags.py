from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user_id, require_admin
from app.schemas.tag import TagCreate, TagOut, TagUpdate
from app.services.tag_service import TagService

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("", response_model=list[TagOut])
async def list_tags(
    db: AsyncSession = Depends(get_db),
    _: int = Depends(get_current_user_id),  # require auth
) -> list[TagOut]:
    svc = TagService(db)
    tags = await svc.list_tags()
    return [TagOut.model_validate(t) for t in tags]


@router.post("", response_model=TagOut, status_code=status.HTTP_201_CREATED)
async def create_tag(
    data: TagCreate,
    db: AsyncSession = Depends(get_db),
    _: int = Depends(get_current_user_id),
) -> TagOut:
    svc = TagService(db)
    if await svc.get_by_name(data.name):
        raise HTTPException(status_code=400, detail="Tag with this name already exists")
    tag = await svc.create_tag(data)
    return TagOut.model_validate(tag)


@router.patch("/{tag_id}", response_model=TagOut, dependencies=[Depends(require_admin)])
async def update_tag(
    tag_id: int,
    data: TagUpdate,
    db: AsyncSession = Depends(get_db),
) -> TagOut:
    svc = TagService(db)
    tag = await svc.get_by_id(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag = await svc.update_tag(tag, data)
    return TagOut.model_validate(tag)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)) -> None:
    svc = TagService(db)
    tag = await svc.get_by_id(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    await svc.delete_tag(tag)
