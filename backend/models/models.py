from datetime import date, datetime

from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.dependencies import metadata, mapper_registry


@mapper_registry.as_declarative_base()
class Base:
    pass


artwork_tag_association = Table(
    "artwork_tag",
    metadata,
    Column("artwork_id", ForeignKey("artwork.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)


class Category(Base):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    artworks: Mapped[list["Artwork"]] = relationship(
        back_populates="category",
        cascade="save-update, delete, delete-orphan"
    )

    id: Mapped[int | None] = mapped_column(
        primary_key=True,
        autoincrement=True
    )



class Artwork(Base):
    __tablename__ = "artwork"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    poster_url: Mapped[str] = mapped_column(nullable=False)
    release_date: Mapped[date] = mapped_column(nullable=False)
    age_rating: Mapped[str] = mapped_column(String(3), nullable=False)
    star_rating: Mapped[float] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"))
    category: Mapped[Category] = relationship(back_populates="artworks", passive_deletes=True)

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="artwork",
        cascade="save-update, delete, delete-orphan"
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="artwork",
        cascade="save-update, delete, delete-orphan"
    )

    tags: Mapped[list["Tag"]] = relationship(
        secondary=artwork_tag_association,
        back_populates="artworks"
    )

    id: Mapped[int | None] = mapped_column(
        primary_key=True,
        autoincrement=True
    )


class User(Base):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author",
        cascade="save-update, delete, delete-orphan"
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="author",
        cascade="save-update, delete, delete-orphan"
    )

    id: Mapped[int | None] = mapped_column(
        primary_key=True,
        autoincrement=True
    )


class Comment(Base):
    __tablename__ = "comment"

    text: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(nullable=False)
    dislikes: Mapped[int] = mapped_column(nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    author: Mapped[User] = relationship(
        back_populates="comments",
        passive_deletes=True
    )

    artwork_id: Mapped[int] = mapped_column(ForeignKey("artwork.id", ondelete="CASCADE"))
    artwork: Mapped[Artwork] = relationship(
        back_populates="comments",
        passive_deletes=True
    )

    id: Mapped[int | None] = mapped_column(
        primary_key=True,
        autoincrement=True
    )


class Review(Base):
    __tablename__ = "review"

    text: Mapped[str] = mapped_column(nullable=False)
    score: Mapped[float] = mapped_column(nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    author: Mapped[User] = relationship(
        back_populates="reviews",
        passive_deletes=True
    )

    artwork_id: Mapped[int] = mapped_column(ForeignKey("artwork.id", ondelete="CASCADE"))
    artwork: Mapped[Artwork] = relationship(
        back_populates="reviews",
        passive_deletes=True
    )

    id: Mapped[int | None] = mapped_column(
        primary_key=True,
        autoincrement=True
    )


class Tag(Base):
    __tablename__ = "tag"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    artworks: Mapped[list[Artwork]] = relationship(
        secondary=artwork_tag_association,
        back_populates="tags"
    )

    id: Mapped[int | None] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
