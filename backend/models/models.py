from datetime import date, datetime

from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.dependencies import metadata, mapper_registry

artwork_tag_association = Table(
    "artwork_tag",
    metadata,
    Column("artwork_id", ForeignKey("artwork.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


@mapper_registry.mapped_as_dataclass
class Category:
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    artworks: Mapped[list["Artwork"]] = relationship(
        default_factory=lambda: [],
        cascade="save-update, delete, delete-orphan"
    )

    id: Mapped[int | None] = mapped_column(
        default_factory=lambda: None,
        primary_key=True,
        autoincrement=True
    )


@mapper_registry.mapped_as_dataclass
class Artwork:
    __tablename__ = "artwork"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    poster_url: Mapped[str] = mapped_column(nullable=False)
    release_date: Mapped[date] = mapped_column(nullable=False)
    age_rating: Mapped[str] = mapped_column(String(3), nullable=False)
    star_rating: Mapped[float] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

    comments: Mapped[list["Comment"]] = relationship(
        default_factory=lambda: [],
        cascade="save-update, delete, delete-orphan"
    )

    reviews: Mapped[list["Review"]] = relationship(
        default_factory=lambda: [],
        cascade="save-update, delete, delete-orphan"
    )

    tags: Mapped[list["Tag"]] = relationship(
        secondary=artwork_tag_association,
        back_populates="artworks",
        default_factory=lambda: []
    )

    id: Mapped[int | None] = mapped_column(
        default_factory=lambda: None,
        primary_key=True,
        autoincrement=True
    )


@mapper_registry.mapped_as_dataclass
class User:
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    comments: Mapped[list["Comment"]] = relationship(
        default_factory=lambda: [],
        cascade="save-update, delete, delete-orphan"
    )

    reviews: Mapped[list["Review"]] = relationship(
        default_factory=lambda: [],
        cascade="save-update, delete, delete-orphan"
    )

    id: Mapped[int | None] = mapped_column(
        default_factory=lambda: None,
        primary_key=True,
        autoincrement=True
    )


@mapper_registry.mapped_as_dataclass
class Comment:
    __tablename__ = "comment"

    text: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(nullable=False)
    dislikes: Mapped[int] = mapped_column(nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    artwork_id: Mapped[int] = mapped_column(ForeignKey("artwork.id"))

    id: Mapped[int | None] = mapped_column(
        default_factory=lambda: None,
        primary_key=True,
        autoincrement=True
    )


@mapper_registry.mapped_as_dataclass
class Review:
    __tablename__ = "review"

    text: Mapped[str] = mapped_column(nullable=False)
    score: Mapped[float] = mapped_column(nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    artwork_id: Mapped[int] = mapped_column(ForeignKey("artwork.id"))

    id: Mapped[int | None] = mapped_column(
        default_factory=lambda: None,
        primary_key=True,
        autoincrement=True
    )


@mapper_registry.mapped_as_dataclass
class Tag:
    __tablename__ = "tag"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    artworks: Mapped[list[Artwork]] = relationship(
        secondary=artwork_tag_association,
        back_populates="tags",
        default_factory=lambda: [],
        cascade="save-update, delete"
    )

    id: Mapped[int | None] = mapped_column(
        default_factory=lambda: None,
        primary_key=True,
        autoincrement=True
    )
