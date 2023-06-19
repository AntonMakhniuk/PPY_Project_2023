from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from backend import crud
from backend import schemas
from backend.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Tag, status_code=status.HTTP_201_CREATED)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    check_tag = crud.get_tag_by_name(db, tag.name)

    if check_tag:
        raise HTTPException(status_code=409, detail="Tag with such name already exists")

    return crud.create_tag(db, tag)


@router.get("/", response_model=list[schemas.Tag])
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tags(db, skip=skip, limit=limit)


@router.get("/{tag_id}", response_model=schemas.Tag)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = crud.get_tag_by_id(db, tag_id)

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    return tag


@router.put("/{tag_id}", response_model=schemas.Tag)
def update_tag(tag_id: int, tag_schema_updated: schemas.TagUpdate, db: Session = Depends(get_db)):
    check_tag = crud.get_tag_by_id(db, tag_id)

    if check_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    return crud.update_tag_base(db, tag_id, tag_schema_updated)


@router.delete("/{tag_id}", response_model=schemas.Tag)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    check_tag = crud.get_tag_by_id(db, tag_id)

    if check_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    check_tag = crud.delete_tag(db, tag_id)

    return check_tag
