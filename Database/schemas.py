from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column, registry

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


artwork_tag_association = Table(
    "artwork_tag",
    metadata,
    Column("artwork_id", ForeignKey("artwork.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


@mapper_registry.mapped_as_dataclass
class Category:
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    artworks: Mapped[list["Artwork"]] = relationship(
        back_populates="category",
        default_factory=lambda: [],
        cascade="save-update, delete, delete-orphan"
    )


@mapper_registry.mapped_as_dataclass
class Artwork:
    __tablename__ = "artwork"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    poster_url: Mapped[str] = mapped_column(nullable=False)
    release_date: Mapped[date] = mapped_column(nullable=False)
    age_rating: Mapped[str] = mapped_column(String(3), nullable=False)
    star_rating: Mapped[float] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped[Category] = relationship(back_populates="artworks")

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="artwork",
        default_factory=lambda: [],
        cascade="save-update, delete, delete-orphan"
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="artwork",
        default_factory=lambda: [],
        cascade="save-update, delete, delete-orphan"
    )

    tags: Mapped[list["Tag"]] = relationship(
        secondary=artwork_tag_association,
        back_populates="artworks",
        default_factory=lambda: []
    )


@mapper_registry.mapped_as_dataclass
class User:
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[date] = mapped_column(nullable=False)

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author",
        default_factory=lambda: [],
        cascade="save-update, delete, delete-orphan"
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="author",
        default_factory=lambda: [],
        cascade="save-update, delete, delete-orphan"
    )


@mapper_registry.mapped_as_dataclass
class Comment:
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(nullable=False)
    dislikes: Mapped[int] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped[User] = relationship(back_populates="comments")

    artwork_id: Mapped[int] = mapped_column(ForeignKey("artwork.id"))
    artwork: Mapped[Artwork] = relationship(back_populates="comments")


@mapper_registry.mapped_as_dataclass
class Review:
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    score: Mapped[float] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped[User] = relationship(back_populates="reviews")

    artwork_id: Mapped[int] = mapped_column(ForeignKey("artwork.id"))
    artwork: Mapped[Artwork] = relationship(back_populates="reviews")


@mapper_registry.mapped_as_dataclass
class Tag:
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    artworks: Mapped[list[Artwork]] = relationship(
        secondary=artwork_tag_association,
        back_populates="tags",
        default_factory=lambda: [],
        cascade="save-update, delete"
    )


DB_URL = "sqlite:///database.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)
connection = engine.connect()
metadata.create_all(bind=engine)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


