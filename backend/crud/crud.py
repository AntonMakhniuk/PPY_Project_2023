from datetime import datetime
from typing import Type

from sqlalchemy.orm import Session, joinedload
from backend import models, schemas


# CRUD functions for USER table
def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[models.User]]:
    return db.query(models.User).options(
        joinedload(models.User.comments),
        joinedload(models.User.reviews)
    ).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, user_login: str) -> models.User | None:
    return db.query(models.User).filter(models.User.login == user_login).first()


def get_user_by_email(db: Session, user_login: str) -> models.User | None:
    return db.query(models.User).filter(models.User.login == user_login).first()


def create_user(db: Session, user_schema: schemas.UserCreate) -> models.User:
    user_model = models.User(**user_schema.dict(), created_at=datetime.now())

    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model


def update_user_base(db: Session, user_id: int, user_schema_updated: schemas.UserUpdate) -> models.User:
    query = db.query(models.User)
    user_model = query.filter(models.User.id == user_id).one()
    update_data = user_schema_updated.dict(exclude_unset=True)

    query.filter(models.User.id == user_id).update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(user_model)

    return user_model


def delete_user(db: Session, user_id: int) -> models.User | None:
    query = db.query(models.User).filter(models.User.id == user_id)
    check_user = query.first()
    db.expire_on_commit = False

    query.delete(synchronize_session=False)
    db.commit()

    db.expire_on_commit = True

    return check_user


# CRUD functions for COMMENT table
def get_all_comments(db: Session, skip: int = 0, limit: int = 100) -> list[Type[models.Comment]]:
    return db.query(models.Comment).offset(skip).limit(limit).all()


def get_comments_from_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Type[models.Comment]]:
    return db.query(models.Comment).filter(models.Comment.author_id == user_id).offset(skip).limit(limit).all()


def get_comments_from_artwork(db: Session, artwork_id: int, skip: int = 0, limit: int = 100) -> list[Type[models.Comment]]:
    return db.query(models.Comment).filter(models.Comment.artwork_id == artwork_id).offset(skip).limit(limit).all()


def get_comment_by_id(db: Session, comment_id: int) -> models.Comment | None:
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def create_comment(db: Session, comment_schema: schemas.CommentCreate, user_id: int, artwork_id: int) -> models.Comment:
    comment_model = models.Comment(**comment_schema.dict(), author_id=user_id, artwork_id=artwork_id)

    db.add(comment_model)
    db.commit()
    db.refresh(comment_model)
    return comment_model


def update_comment_base(db: Session, comment_id: int, comment_schema_updated: schemas.CommentUpdate) -> models.Comment:
    query = db.query(models.Comment)
    comment_model = query.filter(models.Comment.id == comment_id).one()
    update_data = comment_schema_updated.dict(exclude_unset=True)

    query.filter(models.Comment.id == comment_id).update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(comment_model)

    return comment_model


def delete_comment(db: Session, comment_id: int) -> models.Comment | None:
    query = db.query(models.Comment).filter(models.Comment.id == comment_id)
    check_comment = query.first()
    db.expire_on_commit = False

    query.delete(synchronize_session=False)
    db.commit()

    db.expire_on_commit = True

    return check_comment


# CRUD functions for REVIEW table
def get_all_reviews(db: Session, skip: int = 0, limit: int = 100) -> list[Type[models.Review]]:
    return db.query(models.Review).offset(skip).limit(limit).all()


def get_reviews_from_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Type[models.Review]]:
    return db.query(models.Review).filter(models.Review.author_id == user_id).offset(skip).limit(limit).all()


def get_reviews_from_artwork(db: Session, artwork_id: int, skip: int = 0, limit: int = 100) -> list[Type[models.Review]]:
    return db.query(models.Review).filter(models.Review.artwork_id == artwork_id).offset(skip).limit(limit).all()


def get_review_by_id(db: Session, review_id: int) -> models.Review | None:
    return db.query(models.Review).filter(models.Review.id == review_id).first()


def create_review(db: Session, review_schema: schemas.ReviewCreate, user_id: int, artwork_id: int) -> models.Review:
    review_model = models.Review(**review_schema.dict(), author_id=user_id, artwork_id=artwork_id)

    db.add(review_model)
    db.commit()
    db.refresh(review_model)
    return review_model


def update_review_base(db: Session, review_id: int, review_schema_updated: schemas.ReviewUpdate) -> models.Review:
    query = db.query(models.Review)
    review_model = query.filter(models.Review.id == review_id).one()
    update_data = review_schema_updated.dict(exclude_unset=True)

    query.filter(models.Comment.id == review_id).update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(review_model)

    return review_model


def delete_review(db: Session, review_id: int) -> models.Review | None:
    query = db.query(models.Comment).filter(models.Review.id == review_id)
    check_review = query.first()
    db.expire_on_commit = False

    query.delete(synchronize_session=False)
    db.commit()

    db.expire_on_commit = True

    return check_review


# CRUD functions for ARTWORK table
def get_all_artworks(db: Session, skip: int = 0, limit: int = 100) -> list[Type[models.Artwork]]:
    return db.query(models.Artwork).offset(skip).limit(limit).all()


def get_artworks_from_category(db: Session, category_id: int, skip: int = 0, limit: int = 100) -> list[Type[models.Artwork]]:
    return db.query(models.Artwork).filter(models.Artwork.category_id == category_id).offset(skip).limit(limit).all()


def get_artwork_by_id(db: Session, artwork_id: int) -> models.Artwork | None:
    return db.query(models.Artwork).filter(models.Artwork.id == artwork_id).first()


def create_artwork(db: Session, category_id: int, artwork_schema: schemas.ArtworkCreate) -> models.Artwork:
    artwork_model = models.Artwork(
        title=artwork_schema.title,
        description=artwork_schema.description,
        poster_url=artwork_schema.poster_url,
        release_date=artwork_schema.release_date,
        age_rating=artwork_schema.age_rating,
        star_rating=artwork_schema.star_rating,
        category_id=category_id
    )

    db.add(artwork_model)
    db.commit()
    db.refresh(artwork_model)

    return artwork_model

def update_artwork_base(db: Session, artwork_id: int, artwork_schema_updated: schemas.ArtworkUpdate) -> models.Artwork:
    query = db.query(models.Artwork)
    artwork_model = query.filter(models.Artwork.id == artwork_id).one()
    update_data = artwork_schema_updated.dict(exclude_unset=True)

    query.filter(models.Artwork.id == artwork_id).update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(artwork_model)

    return artwork_model


def artwork_add_tag(db: Session, artwork_id: int, tag_id: int) -> models.Artwork:
    artwork_model = db.query(models.Artwork).filter(models.Artwork.id == artwork_id).one()
    tag_model = db.query(models.Tag).filter(models.Tag.id == tag_id).one()
    artwork_model.tags.add(tag_model)

    db.commit()
    db.refresh(artwork_model)

    return artwork_model


def artwork_remove_tag(db: Session, artwork_id: int, tag_id: int) -> models.Artwork:
    artwork_model = db.query(models.Artwork).filter(models.Artwork.id == artwork_id).one()
    tag_model = db.query(models.Tag).filter(models.Tag.id == tag_id).one()
    artwork_model.tags.remove(tag_model)

    db.commit()
    db.refresh(artwork_model)

    return artwork_model


def delete_artwork(db: Session, artwork_id: int) -> models.Artwork | None:
    query = db.query(models.Artwork).filter(models.Artwork.id == artwork_id)
    check_artwork = query.first()
    db.expire_on_commit = False

    query.delete(synchronize_session=False)
    db.commit()

    db.expire_on_commit = True

    return check_artwork


# CRUD functions for TAG table
def get_tags(db: Session, skip: int = 0, limit: int = 100) -> list[Type[models.Tag]]:
    return db.query(models.Tag).options(joinedload(models.Tag.artworks)).offset(skip).limit(limit).all()


def get_tag_by_id(db: Session, tag_id: int) -> models.Tag | None:
    return db.query(models.Tag).options(joinedload(models.Tag.artworks)).filter(models.Tag.id == tag_id).first()


def get_tag_by_name(db: Session, tag_name: str) -> models.Tag | None:
    return db.query(models.Tag).options(joinedload(models.Tag.artworks)).filter(models.Tag.id == tag_name).first()


def create_tag(db: Session, tag_schema: schemas.TagCreate) -> models.Tag:
    tag_model = models.Tag(
        name=tag_schema.name,
        description=tag_schema.description,
    )

    db.add(tag_model)
    db.commit()
    db.refresh(tag_model)

    return tag_model


def update_tag_base(db: Session, tag_id: int, tag_schema_updated: schemas.TagUpdate) -> models.Tag:
    query = db.query(models.Tag)
    tag_model = query.filter(models.Tag.id == tag_id).one()
    update_data = tag_schema_updated.dict(exclude_unset=True)

    query.filter(models.Tag.id == tag_id).update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(tag_model)

    return tag_model


def delete_tag(db: Session, tag_id: int) -> models.Tag | None:
    query = db.query(models.Tag).filter(models.Tag.id == tag_id)
    check_tag = query.first()
    db.expire_on_commit = False

    query.delete(synchronize_session=False)
    db.commit()

    db.expire_on_commit = True

    return check_tag


# CRUD functions for CATEGORY table
def get_categories(db: Session, skip: int = 0, limit: int = 100) -> list[Type[models.Category]]:
    return db.query(models.Category).options(joinedload(models.Category.artworks)).offset(skip).limit(limit).all()


def get_category_by_id(db: Session, category_id: int) -> models.Category | None:
    return db.query(models.Category) \
        .options(joinedload(models.Category.artworks)).filter(models.Category.id == category_id).first()


def get_category_by_name(db: Session, category_name: str) -> models.Category | None:
    return db.query(models.Category) \
        .options(joinedload(models.Category.artworks)).filter(models.Category.name == category_name).first()


def create_category(db: Session, category_schema: schemas.CategoryCreate) -> models.Category:
    category_model = models.Category(
        name=category_schema.name,
        description=category_schema.description,
    )

    db.add(category_model)
    db.commit()
    db.refresh(category_model)

    return category_model


def update_category_base(db: Session, category_id: int,
                         category_schema_updated: schemas.CategoryUpdate) -> models.Category | None:
    query = db.query(models.Category)
    category_model = query.filter(models.Category.id == category_id).first()
    update_data = category_schema_updated.dict(exclude_unset=True)

    query.filter(models.Category.id == category_id).update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(category_model)

    return category_model


def delete_category(db: Session, category_id: int) -> models.Category | None:
    query = db.query(models.Category).filter(models.Category.id == category_id)
    check_category = query.first()
    db.expire_on_commit = False

    query.delete(synchronize_session=False)
    db.commit()

    db.expire_on_commit = True

    return check_category
