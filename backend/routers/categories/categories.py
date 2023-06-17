from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    check_category = crud.get_category_by_name(db, category.name)

    if check_category:
        raise HTTPException(status_code=409, detail="Category with such name already exists")

    return crud.create_category(db, category)


@router.get("/", response_model=list[schemas.Category])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categories(db, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=schemas.Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category_by_id(db, category_id)

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category_schema_updated: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    check_category = crud.get_category_by_id(db, category_id)

    if check_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    check_category = crud.get_category_by_name(db, category_schema_updated.name)

    if check_category:
        raise HTTPException(status_code=409, detail="Category with such name already exists")

    return crud.update_category_base(db, category_id, category_schema_updated)


@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    check_category = crud.get_category_by_id(db, category_id)

    if check_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    check_category = crud.delete_category(db, category_id)

    return check_category


@router.post("/{category_id}/artworks", response_model=schemas.Artwork, status_code=status.HTTP_201_CREATED)
def create_artwork(category_id: int, artwork: schemas.ArtworkCreate, db: Session = Depends(get_db)):
    category = crud.get_category_by_id(db, category_id)

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return crud.create_artwork(db, category_id, artwork)
