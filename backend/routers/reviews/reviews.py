from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from backend import schemas, crud
from backend.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.Review])
def get_all_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_reviews(db, skip=skip, limit=limit)


@router.get("/{review_id}", response_model=schemas.Review)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = crud.get_review_by_id(db, review_id)

    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    return review


@router.put("/{review_id}", response_model=schemas.Review)
def update_review(review_id: int, review_schema_updated: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    check_review = crud.get_review_by_id(db, review_id)

    if check_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    return crud.update_review_base(db, review_id, review_schema_updated)


@router.delete("/{review_id}", response_model=schemas.Review)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    check_review = crud.get_review_by_id(db, review_id)

    if check_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    check_review = crud.delete_review(db, review_id)

    return check_review
