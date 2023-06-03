from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl


# Schemas for COMMENT
class CommentBase(BaseModel):
    text: str
    likes: int
    dislikes: int


class CommentUpdate(BaseModel):
    text: Optional[str] = None
    likes: Optional[int] = None
    dislikes: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    author_id: int
    artwork_id: int

    class Config:
        orm_mode = True


# Schemas for REVIEW
class ReviewBase(BaseModel):
    text: str
    score: float


class ReviewUpdate(BaseModel):
    text: Optional[str] = None
    score: Optional[float] = None


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    author_id: int
    artwork_id: int

    class Config:
        orm_mode = True


# Schemas for TAG
class TagBase(BaseModel):
    name: str
    description: str


class TagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    artworks: list["ArtworkBase"]

    class Config:
        orm_mode = True


# Schemas for ARTWORK
class ArtworkBase(BaseModel):
    title: str
    description: str
    poster_url: HttpUrl
    release_date: date
    age_rating: str
    star_rating: float


class ArtworkUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    poster_url: Optional[HttpUrl] = None
    release_date: Optional[date] = None
    age_rating: Optional[str] = None
    star_rating: Optional[float] = None


class ArtworkCreate(ArtworkBase):
    pass


class Artwork(ArtworkBase):
    id: int
    category_id: int
    comments: list[Comment]
    reviews: list[Review]
    tags: list[TagBase]

    class Config:
        orm_mode = True


Tag.update_forward_refs(ArtworkBase=ArtworkBase)


# Schemas for CATEGORY
class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    artworks: list[ArtworkBase]

    class Config:
        orm_mode = True


# Schemas for USER
class UserBase(BaseModel):
    login: str
    password: str
    email: EmailStr


class UserUpdate(BaseModel):
    password: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    comments: list[Comment]
    reviews: list[Review]

    class Config:
        orm_mode = True
