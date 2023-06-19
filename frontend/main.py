from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates
import requests

from starlette.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from starlette.templating import _TemplateResponse

from backend.dependencies import close_db_state, db_state, metadata
# from backend.dependencies import close_connection, engine, metadata
from backend.routers import artworks as artworks_router
from backend.routers import tags as tags_router, categories as categories_router, reviews as reviews_router, \
    users as users_router, comments as comments_router
from backend.dependencies import get_db
from backend.schemas import User
from backend.schemas import UserCreate

app = FastAPI(
    on_startup=[lambda: metadata.create_all(bind=db_state.engine)],
    on_shutdown=[lambda: close_db_state(db_state)],
)

tags_metadata = [
    {
        "name": "crud - tags",
        "description": "CRUD operations for TAG table (data for tags)."
    },
    {
        "name": "crud - categories",
        "description": "CRUD operations for CATEGORY table (data for categories)."
    },
    {
        "name": "crud - artworks",
        "description": "CRUD operations for ARTWORK table (data for artworks)."
    },
    {
        "name": "crud - comments",
        "description": "CRUD operations for COMMENT table (data for comments)."
    },
    {
        "name": "crud - reviews",
        "description": "CRUD operations for REVIEWS table (data for reviews)."
    },
    {
        "name": "crud - users",
        "description": "CRUD operations for USER table (data for users)."
    },
]

app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(router=tags_router.router, prefix="/tags", tags=["crud - tags"])
app.include_router(router=categories_router.router, prefix="/categories", tags=["crud - categories"])
app.include_router(router=artworks_router.router, prefix="/artworks", tags=["crud - artworks"])
app.include_router(router=comments_router.router, prefix="/comments", tags=["crud - comments"])
app.include_router(router=reviews_router.router, prefix="/reviews", tags=["crud - reviews"])
app.include_router(router=users_router.router, prefix="/users", tags=["crud - users"])


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/home", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.post("/login", status_code=status.HTTP_200_OK)
def login(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.login == user.login).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if db_user.password != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return templates.TemplateResponse("login.html", {"request": request})


# Route for artworks
@app.get("/get-categories/{category_id}/artworks", response_class=HTMLResponse)
def show_artworks_in_category(request: Request, category_id: int):
    artwork_data = {
        "title": "string",
        "description": "string",
        "poster_url": "string",
        "release_date": "2023-06-19",
        "age_rating": "string",
        "star_rating": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/categories/{category_id}/artworks", json=artwork_data)
    new_artwork = response.json()
    return templates.TemplateResponse("artworks", {"request": request, "artwork": new_artwork})


@app.get("/get-artworks", response_class=HTMLResponse)
def show_artworks(request: Request):
    artwork_data = {
        "title": "string",
        "description": "string",
        "poster_url": "string",
        "release_date": "2023-06-19",
        "age_rating": "string",
        "star_rating": 0,
        "id": 0,
        "category_id": 0,
        "comments": [
            {
                "text": "string",
                "likes": 0,
                "dislikes": 0,
                "id": 0,
                "author_id": 0,
                "artwork_id": 0
            }
        ],
        "reviews": [
            {
                "text": "string",
                "score": 0,
                "id": 0,
                "author_id": 0,
                "artwork_id": 0
            }
        ],
        "tags": [
            {
                "name": "string",
                "description": "string"
            }
        ]
    }
    response = requests.get("http://127.0.0.1:8000/artworks", json=artwork_data)
    new_artwork = response.json()
    return templates.TemplateResponse("artworks.html", {"request": request, "artwork": new_artwork})


@app.get("/get-artworks/{artwork_id}", response_class=HTMLResponse)
def get_artwork(request: Request):
    artwork_id = {
        "title": "string",
        "description": "string",
        "poster_url": "string",
        "release_date": "2023-06-19",
        "age_rating": "string",
        "star_rating": 0,
        "id": 0,
        "category_id": 0,
        "comments": [
            {
                "text": "string",
                "likes": 0,
                "dislikes": 0,
                "id": 0,
                "author_id": 0,
                "artwork_id": 0
            }
        ],
        "reviews": [
            {
                "text": "string",
                "score": 0,
                "id": 0,
                "author_id": 0,
                "artwork_id": 0
            }
        ],
        "tags": [
            {
                "name": "string",
                "description": "string"
            }
        ]
    }
    response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}")
    artwork_data = response.json()
    return templates.TemplateResponse("artworks-single.html", {"request": request, "artwork": artwork_data})


@app.get("/get-artworks/{artwork_id}/comments", response_class=HTMLResponse)
def get_artwork_comments(request: Request, artwork_id: int):
    artwork_data = {

        "text": "string",
        "likes": 0,
        "dislikes": 0,
        "id": 0,
        "author_id": 0,
        "artwork_id": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}/comments", json=artwork_data)
    artwork_data = response.json()
    return templates.TemplateResponse("artowrk-single.html", {"request": request, "artwork": artwork_data})


@app.get("/get-artworks/{artwork_id}/reviews", response_class=HTMLResponse)
def get_artwork_reviews(request: Request, artwork_id: int):
    artwork_data = {
        "text": "string",
        "score": 0,
        "id": 0,
        "author_id": 0,
        "artwork_id": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}/reviews", json=artwork_data)
    artwork_data = response.json()
    return templates.TemplateResponse("artwork_review.html", {"request": request, "artwork": artwork_data})


# Route for categories
@app.get("/get-categories", response_class=HTMLResponse)
def show_categories(request: Request):
    category_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/categories", json=category_data)
    new_category = response.json()
    return templates.TemplateResponse("categorys.html", {"request": request, "category": new_category})


@app.get("/get-categories-index", response_class=HTMLResponse)
def show_categories_for_home(request: Request):
    category_data = {
        "name": "string",
        "description": "string",
        "id": 0,
        "artworks": [
            {
                "title": "string",
                "description": "string",
                "poster_url": "string",
                "release_date": "2023-06-19",
                "age_rating": "string",
                "star_rating": 0
            }
        ]
    }
    response = requests.get("http://127.0.0.1:8000/categories", json=category_data)
    new_category = response.json()
    return templates.TemplateResponse("index.html", {"request": request, "category": new_category})


@app.get("/get-categories/{category_id}", response_class=HTMLResponse)
def get_category(request: Request, category_id: int):
    category_data = {
        "name": "string",
        "description": "string",
        "id": 0,
        "artworks": [
            {
                "title": "string",
                "description": "string",
                "poster_url": "string",
                "release_date": "2023-06-09",
                "age_rating": "string",
                "star_rating": 0
            }
        ]
    }
    response = requests.get(f"http://127.0.0.1:8000/categories/{category_id}", json=category_data)
    category_data = response.json()
    return templates.TemplateResponse("category.html", {"request": request, "category": category_data})


# Route for comments
@app.post("/get-get-form-comments", response_class=HTMLResponse)
def create_comment(request: Request):
    comment_data = {
        "text": "string",
        "likes": 0,
        "dislikes": 0,
        "id": 0,
        "author_id": 0,
        "artwork_id": 0
    }
    response = requests.post("http://127.0.0.1:8000/comments", json=comment_data)
    new_comment = response.json()
    return templates.TemplateResponse("comment_create.html", {"request": request, "comment": new_comment})


@app.get("/get-get-comments", response_class=HTMLResponse)
def create_comment(request: Request):
    comment_data = {
        "text": "string",
        "likes": 0,
        "dislikes": 0,
        "id": 0,
        "author_id": 0,
        "artwork_id": 0
    }
    response = requests.get("http://127.0.0.1:8000/comments", json=comment_data)
    new_comment = response.json()
    return templates.TemplateResponse("comment_create.html", {"request": request, "comment": new_comment})


@app.get("/get-comments/{comment_id}", response_class=HTMLResponse)
def get_comment(request: Request, comment_id: int):
    comment_data = {
        "text": "string",
        "likes": 0,
        "dislikes": 0,
        "id": 0,
        "author_id": 0,
        "artwork_id": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/comments/{comment_id}", json=comment_data)
    comment_data = response.json()
    return templates.TemplateResponse("comment.html", {"request": request, "comment": comment_data})


# Route for reviews
@app.get("/get-reviews", response_class=HTMLResponse)
def show_reviews(request: Request):
    review_data = {
        "text": "string",
        "score": 0,
        "id": 0,
        "author_id": 0,
        "artwork_id": 0
    }
    response = requests.get("http://127.0.0.1:8000/reviews", json=review_data)
    new_review = response.json()
    return templates.TemplateResponse("review.html", {"request": request, "review": new_review})


@app.get("/get-reviews/{review_id}", response_class=HTMLResponse)
def get_review(request: Request, review_id: int):
    review_data = {
        "text": "string",
        "score": 0,
        "id": 0,
        "author_id": 0,
        "artwork_id": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/reviews/{review_id}", json=review_data)
    review_data = response.json()
    return templates.TemplateResponse("review-single.html", {"request": request, "review": review_data})


# Route for tags
@app.get("/get-tags/{tag_id}", response_class=HTMLResponse)
def get_tag(request: Request, tag_id: int):
    tag_data = {
        "name": "string",
        "description": "string",
        "id": 0,
        "artworks": [
            {
                "title": "string",
                "description": "string",
                "poster_url": "string",
                "release_date": "2023-06-09",
                "age_rating": "string",
                "star_rating": 0
            }
        ]
    }
    response = requests.get(f"http://127.0.0.1:8000/tags/{tag_id}", json=tag_data)
    tag_data = response.json()
    return templates.TemplateResponse("tag.html", {"request": request, "tag": tag_data})


@app.get("/get-tags", response_class=HTMLResponse)
def show_tags(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("login.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-index", response_class=HTMLResponse)
def show_tags_i(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("index.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-404", response_class=HTMLResponse)
def show_tags_404(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("404-page.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-about", response_class=HTMLResponse)
def show_tags_a(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("404-page.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-artwork", response_class=HTMLResponse)
def show_tags_art(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("artworks.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-artwork-s", response_class=HTMLResponse)
def show_tags_a_s(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("artworks.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-artwork-sd", response_class=HTMLResponse)
def show_tags_a_sd(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("artworks.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-c", response_class=HTMLResponse)
def show_tags_c(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("categorys.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-r", response_class=HTMLResponse)
def show_tags_r(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("review.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-rs", response_class=HTMLResponse)
def show_tags_rs(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("review-single.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-si", response_class=HTMLResponse)
def show_tags_rs(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("signup.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-us", response_class=HTMLResponse)
def show_tags_rs(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("user-single.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-usc", response_class=HTMLResponse)
def show_tags_rs(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("user-single-comments.html", {"request": request, "tag": new_tag})


@app.get("/get-tags-usr", response_class=HTMLResponse)
def show_tags_rs(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("user-single-review.html", {"request": request, "tag": new_tag})


@app.get("/create-tag-form", response_class=HTMLResponse)
def create_tag(request: Request):
    tag_data = {
        "name": "",
        "description": ""
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("tag_create.html", {"request": request, "tag": new_tag})


@app.post("/create-tag", response_class=HTMLResponse)
def create_tag(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.post("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("tag_create.html", {"request": request, "tag": new_tag})


# Route for users
@app.get("/make-users-form", response_class=HTMLResponse)
def create_user(request: Request):
    user_data = {
        "login": "string",
        "password": "string",
        "email": "user@example.com"
    }
    response = requests.get("http://127.0.0.1:8000/users/", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("signup.html", {"request": request, "user": new_user})


@app.post("/make-users", response_class=HTMLResponse)
def create_user(request: Request):
    user_data = {
        "login": "string",
        "password": "string",
        "email": "user@example.com"
    }
    response = requests.post("http://127.0.0.1:8000/users/", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("signup.html", {"request": request, "user": new_user})


@app.get("/get-users/{user_id}", response_class=HTMLResponse)
def show_user_one(request: Request, user_id: int):
    user_data = {
        "login": "string",
        "password": "string",
        "email": "user@example.com"
    }
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("user-single.html", {"request": request, "user": new_user})


@app.get("/put-users-form/{user_id}", response_class=HTMLResponse)
def update_user(request: Request, user_id: int):
    new_data = {
        "password": "string",
        "email": "user@example.com"
    }
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("update_user.html", {"request": request, "user": updated_user})


@app.put("/put-users/{user_id}", response_class=HTMLResponse)
def update_user(request: Request, user_id: int):
    new_data = {
        "password": "string",
        "email": "user@example.com"
    }
    response = requests.put(f"http://127.0.0.1:8000/users/{user_id}", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("update_user.html", {"request": request, "user": updated_user})


@app.get("/get-users/{user_id}/comments", response_class=HTMLResponse)
def show_user_comment(request: Request, user_id: int):
    user_data = {
        "text": "string",
        "likes": 0,
        "dislikes": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}/comments", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("user-single-comments.html", {"request": request, "user": new_user})


@app.get("/post-users-form/{user_id}/comments", response_class=HTMLResponse)
def create_user_comment(request: Request, user_id: int):
    new_data = {
        "text": "string",
        "likes": 0,
        "dislikes": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}/comments", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("create_user_comment.html", {"request": request, "user": updated_user})


@app.post("/post-users/{user_id}/comments", response_class=HTMLResponse)
def create_user_comment(request: Request, user_id: int):
    new_data = {
        "text": "string",
        "likes": 0,
        "dislikes": 0
    }
    response = requests.post(f"http://127.0.0.1:8000/users/{user_id}/comments", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("create_user_comment.html", {"request": request, "user": updated_user})


@app.get("/get-users/{user_id}/reviews", response_class=HTMLResponse)
def show_user_review(request: Request, user_id: int):
    user_data = {
        "text": "string",
        "score": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}/reviews", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("user-single-review.html", {"request": request, "user": new_user})


@app.post("/post-users/{user_id}/reviews", response_class=HTMLResponse)
def create_user_review(request: Request, user_id: int):
    new_data = {
        "text": "string",
        "score": 0
    }
    response = requests.post(f"http://127.0.0.1:8000/users/{user_id}/reviews", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("create-rewiev.html", {"request": request, "user": updated_user})


@app.get("/post-users-form/{user_id}/reviews", response_class=HTMLResponse)
def create_user_review(request: Request, user_id: int):
    new_data = {
        "text": "string",
        "score": 0
    }
    response = requests.post(f"http://127.0.0.1:8000/users/{user_id}/reviews", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("create-rewiev.html", {"request": request, "user": updated_user})
