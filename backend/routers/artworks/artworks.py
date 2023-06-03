from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from backend import schemas, crud
from backend.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.Artwork])
def get_artworks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_artworks(db, skip=skip, limit=limit)


@router.get("/{artwork_id}", response_model=schemas.Artwork)
def get_artwork(artwork_id: int, db: Session = Depends(get_db)):
    artwork = crud.get_artwork_by_id(db, artwork_id)

    if artwork is None:
        raise HTTPException(status_code=404, detail="Artwork not found")

    return artwork


@router.put("/{artwork_id}", response_model=schemas.Artwork)
def update_artwork(artwork_id: int, artwork_schema_updated: schemas.ArtworkUpdate, db: Session = Depends(get_db)):
    check_artwork = crud.get_artwork_by_id(db, artwork_id)

    if check_artwork is None:
        raise HTTPException(status_code=404, detail="Artwork not found")

    return crud.update_artwork_base(db, artwork_id, artwork_schema_updated)


@router.delete("/{artwork_id}", response_model=schemas.Artwork)
def delete_artwork(artwork_id: int, db: Session = Depends(get_db)):
    check_artwork = crud.get_artwork_by_id(db, artwork_id)

    if check_artwork is None:
        raise HTTPException(status_code=404, detail="Artwork not found")

    check_artwork = crud.delete_artwork(db, artwork_id)

    return check_artwork


@router.get("/{artwork_id}/comments/", response_model=list[schemas.Comment])
def get_comments_from_artwork(artwork_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if crud.get_artwork_by_id(db, artwork_id) is None:
        raise HTTPException(status_code=404, detail="Artwork not found")

    return crud.get_comments_from_artwork(db, artwork_id=artwork_id, skip=skip, limit=limit)


@router.get("/{artwork_id}/reviews/", response_model=list[schemas.Review])
def get_reviews_from_artwork(artwork_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if crud.get_artwork_by_id(db, artwork_id) is None:
        raise HTTPException(status_code=404, detail="Artwork not found")

    return crud.get_reviews_from_artwork(db, artwork_id=artwork_id, skip=skip, limit=limit)
