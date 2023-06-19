from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from backend import crud
from backend import schemas
from backend.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.Comment])
def get_all_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_comments(db, skip=skip, limit=limit)


@router.get("/{comment_id}", response_model=schemas.Comment)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = crud.get_comment_by_id(db, comment_id)

    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment


@router.put("/{comment_id}", response_model=schemas.Comment)
def update_comment(comment_id: int, comment_schema_updated: schemas.CommentUpdate, db: Session = Depends(get_db)):
    check_comment = crud.get_comment_by_id(db, comment_id)

    if check_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return crud.update_comment_base(db, comment_id, comment_schema_updated)


@router.delete("/{comment_id}", response_model=schemas.Comment)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    check_comment = crud.get_comment_by_id(db, comment_id)

    if check_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    check_comment = crud.delete_comment(db, comment_id)

    return check_comment
