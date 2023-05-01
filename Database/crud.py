from typing import Optional, List
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column, registry
from schemas import *


# CRUD functions for ARTWORK table
def create_artwork(id: int, title: str, description: str, poster_url: str, release_date: date, category_id: int,
                   age_rating: str,
                   star_rating: float) -> Artwork:
    session = Session()
    category = session.query(Category).get(category_id)
    artwork = Artwork(id=id, title=title, description=description, poster_url=poster_url, release_date=release_date,
                      category_id=category_id,category=category, age_rating=age_rating, star_rating=star_rating)
    artwork.category = category
    session.add(artwork)
    session.commit()
    return artwork


def read_artwork(artwork_id: int) -> Optional[Artwork]:
    session = Session()
    artwork = session.query(Artwork).get(artwork_id)
    return artwork


def update_artwork(artwork_id: int, title: Optional[str] = None, description: Optional[str] = None,
                   poster_url: Optional[str] = None, release_date: Optional[date] = None,
                   category_id: Optional[int] = None, age_rating: Optional[str] = None,
                   star_rating: Optional[float] = None) -> Optional[Artwork]:
    session = Session()
    artwork = session.query(Artwork).get(artwork_id)
    if artwork:
        if title:
            artwork.title = title
        if description:
            artwork.description = description
        if poster_url:
            artwork.poster_url = poster_url
        if release_date:
            artwork.release_date = release_date
        if category_id:
            artwork.category_id = category_id
        if age_rating:
            artwork.age_rating = age_rating
        if star_rating:
            artwork.StarRating = star_rating
        session.commit()
        return artwork
    return None


def delete_artwork(artwork_id: int) -> bool:
    session = Session()
    artwork = session.query(Artwork).get(artwork_id)
    if artwork:
        session.delete(artwork)
        session.commit()
        return True
    return False


# CRUD functions for CATEGORY table
def create_category(id:int,name: str, description: str) -> Category:
    session = Session()
    category = Category(id=id,name=name, description=description)
    session.add(category)
    session.commit()
    session.refresh(category)
    session.close()
    return category


def get_category(category_id: int) -> Optional[Category]:
    session = Session()
    category = session.query(Category).filter(Category.category_id == category_id).first()
    session.close()
    return category


def update_category(category_id: int, name: str, description: str) -> Optional[Category]:
    session = Session()
    category = session.query(Category).filter(Category.category_id == category_id).first()
    if category:
        category.name = name
        category.description = description
        session.commit()
        session.refresh(category)
    session.close()
    return category


def delete_category(category_id: int) -> Optional[Category]:
    session = Session()
    category = session.query(Category).filter(Category.id == category_id).first()
    if category:
        session.delete(category)
        session.commit()
    session.close()
    return category


# CRUD functions for COMMENT table
def create_comment(id:int,text: str, likes: int, dislikes: int, user_id: int, artwork_id: int) -> Comment:
    session = Session()
    author = session.query(User).get(user_id)
    artwork=session.query(Artwork).get(artwork_id)
    comment = Comment(id=id,text=text, likes=likes, dislikes=dislikes, user_id=user_id,author=author, artwork_id=artwork_id,artwork=artwork)
    comment.artwork=artwork
    comment.author=author
    session.add(comment)
    session.commit()
    session.refresh(comment)
    session.close()
    return comment


def get_comment(comment_id: int) -> Optional[Comment]:
    session = Session()
    comment = session.query(Comment).filter(Comment.comment_id == comment_id).first()
    session.close()
    return comment


def update_comment(comment_id: int, text: str, likes: int, dislikes: int) -> Optional[Comment]:
    session = Session()
    comment = session.query(Comment).filter(Comment.comment_id == comment_id).first()
    if comment:
        comment.text = text
        comment.likes = likes
        comment.dislikes = dislikes
        session.commit()
        session.refresh(comment)
    session.close()
    return comment


def delete_comment(comment_id: int) -> Optional[Comment]:
    session = Session()
    comment = session.query(Comment).filter(Comment.comment_id == comment_id).first()
    if comment:
        session.delete(comment)
        session.commit()
    session.close()
    return comment


# CRUD functions for USER table

def get_user(user_id: int) -> User:
    session = Session()
    user = session.query(User).get(user_id)
    session.close()
    return user


def get_all_users() -> List[User]:
    session = Session()
    users = session.query(User).all()
    session.close()
    return users


def create_user(id:int,login: str, password: str, email: str, created_at: date) -> User:
    session = Session()
    user = User(id=id,login=login, password=password, email=email, created_at=created_at)
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return user


def update_user(user_id: int, login: Optional[str] = None, password: Optional[str] = None, email: Optional[str] = None,
                created_at: Optional[date] = None) -> User:
    session = Session()
    user = session.query(User).get(user_id)
    if user:
        if login:
            user.login = login
        if password:
            user.password = password
        if email:
            user.email = email
        if created_at:
            user.created_at = created_at
        session.commit()
        session.refresh(user)
    session.close()
    return user


def delete_user(user_id: int) -> bool:
    session = Session()
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
        session.close()
        return True
    session.close()
    return False


# CRUD functions for TAG table
def create_tag(id:int,name: str, description: str) -> Tag:
    session = Session()
    tag = Tag(id=id,name=name, description=description)
    session.add(tag)
    session.commit()
    return tag


def read_tag(tag_id: int) -> Tag:
    session = Session()
    tag = session.query(Tag).filter_by(id=tag_id).first()
    session.close()
    return tag


def update_tag(tag_id: int, name: str, description: str) -> Tag:
    session = Session()
    tag = read_tag(tag_id, session)
    if tag:
        tag.name = name
        tag.description = description
        session.commit()
    return tag


def delete_tag(tag_id: int) -> bool:
    session = Session()
    tag = read_tag(tag_id)
    if tag:
        session.delete(tag)
        session.commit()
        return True
    return False


# CRUD functions for REVIEW table
def create_review(id:int,text: str, score: float, user_id: int, artwork_id: int) -> Review:
    session = Session()
    author = session.query(User).get(user_id)
    artwork = session.query(Artwork).get(artwork_id)
    review = Review(id=id,text=text, score=score, user_id=user_id,author=author, artwork_id=artwork_id,artwork=artwork)
    review.artwork = artwork
    review.author = author
    session.add(review)
    session.commit()
    return review


def read_review(review_id: int) -> Review:
    session = Session()
    review = session.query(Review).filter_by(recommendation_id=review_id).first()
    return review


def update_review(review_id: int, text: str, score: float, user_id: int, artwork_id: int) -> Review:
    session = Session()
    review = read_review(review_id, session)
    if review:
        review.text = text
        review.score = score
        review.USER_id = user_id
        review.ARTWORK_id = artwork_id
        session.commit()
    return review


def delete_review(review_id: int) -> bool:
    session = Session()
    review = read_review(review_id, session)
    if review:
        session.delete(review)
        session.commit()
        return True
    return False