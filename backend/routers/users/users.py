from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from backend import schemas, crud
from backend.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    check_user = crud.get_user_by_login(db, user.login)

    if check_user:
        raise HTTPException(status_code=409, detail="User with such name already exists")

    check_user = crud.get_user_by_email(db, user.email)

    if check_user:
        raise HTTPException(status_code=409, detail="User with such email already exists")

    return crud.create_user(db, user)


@router.get("/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_schema_updated: schemas.UserUpdate, db: Session = Depends(get_db)):
    check_user = crud.get_user_by_id(db, user_id)

    if check_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.update_user_base(db, user_id, user_schema_updated)


@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    check_user = crud.get_user_by_id(db, user_id)

    if check_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    check_user = crud.delete_user(db, user_id)

    return check_user


@router.get("/{user_id}/comments/", response_model=list[schemas.Comment])
def get_comments_from_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if crud.get_user_by_id(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_comments_from_user(db, user_id=user_id, skip=skip, limit=limit)


@router.post("/{user_id}/comments/", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED)
def create_comment(user_id: int, artwork_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_id(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    if crud.get_artwork_by_id(db, artwork_id) is None:
        raise HTTPException(status_code=404, detail="Artwork not found")

    return crud.create_comment(db, user_id=user_id, artwork_id=artwork_id, comment_schema=comment)


@router.get("/{user_id}/reviews/", response_model=list[schemas.Review])
def get_reviews_from_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if crud.get_user_by_id(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_reviews_from_user(db, user_id=user_id, skip=skip, limit=limit)


@router.post("/{user_id}/reviews/", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
def create_review(user_id: int, artwork_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_id(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    if crud.get_artwork_by_id(db, artwork_id) is None:
        raise HTTPException(status_code=404, detail="Artwork not found")

    user_reviews = crud.get_reviews_from_user(db, user_id=user_id)

    if any(review.artwork_id == artwork_id for review in user_reviews):
        raise HTTPException(status_code=400, detail="User with this id already has a review for artwork with this id")

    return crud.create_review(db, user_id=user_id, artwork_id=artwork_id, review_schema=review)

