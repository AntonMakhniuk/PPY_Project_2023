from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
from starlette.staticfiles import StaticFiles

from backend.dependencies import close_connection, engine, metadata
from backend.routers import tags as tags_router
from backend.routers import categories as categories_router
from backend.routers import artworks as artworks_router
from backend.routers import comments as comments_router
from backend.routers import reviews as reviews_router
from backend.routers import users as users_router

app = FastAPI(
    on_startup=[lambda: metadata.create_all(bind=engine)],
    on_shutdown=[lambda: close_connection()],
)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

app.include_router(router=tags_router.router, prefix="/tags")
app.include_router(router=categories_router.router, prefix="/categories")
app.include_router(router=artworks_router.router, prefix="/artworks")
app.include_router(router=comments_router.router, prefix="/comments")
app.include_router(router=reviews_router.router, prefix="/reviews")
app.include_router(router=users_router.router, prefix="/users")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# Route for artworks
@app.get("/get-categories/{category_id}/artworks")
def show_artworks_in_category(request: Request, artwork_data: dict, category_id: int):
    response = requests.get(f"http://127.0.0.1:8000/categories/{category_id}/artworks", json=artwork_data)
    new_artwork = response.json()
    return templates.TemplateResponse("show_artwork.html", {"request": request, "artwork": new_artwork})


@app.get("/post-categories-form/{category_id}/artworks")
def create_artworks_in_category(request: Request, category_id: int):
    artwork_data = {
        "title": "string",
        "description": "string",
        "poster_url": "string",
        "release_date": "2023-06-09",
        "age_rating": "string",
        "star_rating": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/categories/{category_id}/artworks", json=artwork_data)
    new_artwork = response.json()
    return templates.TemplateResponse("create_artwork.html", {"request": request, "artwork": new_artwork})


@app.post("/post-categories/{category_id}/artworks")
def create_artworks_in_category(request: Request, category_id: int):
    artwork_data = {
        "title": "string",
        "description": "string",
        "poster_url": "string",
        "release_date": "2023-06-09",
        "age_rating": "string",
        "star_rating": 0
    }
    response = requests.post(f"http://127.0.0.1:8000/categories/{category_id}/artworks", json=artwork_data)
    new_artwork = response.json()
    return templates.TemplateResponse("create_artwork.html", {"request": request, "artwork": new_artwork})


@app.get("/get-artworks")
def show_artworks(request: Request):
    artwork_data = {
        "title": "string",
        "description": "string",
        "poster_url": "string",
        "release_date": "2023-06-09",
        "age_rating": "string",
        "star_rating": 0,
        "id": 0,
        "category_id": 0,
        "comments":
            {
                "text": "string",
                "likes": 0,
                "dislikes": 0,
                "id": 0,
                "author_id": 0,
                "artwork_id": 0
            }
        ,
        "reviews":
            {
                "text": "string",
                "score": 0,
                "id": 0,
                "author_id": 0,
                "artwork_id": 0
            }
        ,
        "tags":
            {
                "name": "string",
                "description": "string"
            }

    }
    response = requests.get("http://127.0.0.1:8000/artworks", json=artwork_data)
    new_artwork = response.json()
    return templates.TemplateResponse("artworks.html", {"request": request, "artwork": new_artwork})


@app.get("/get-artworks/{artwork_id}")
def get_artwork(request: Request):
    artwork_id = {
        "title": "string",
        "description": "string",
        "poster_url": "string",
        "release_date": "2023-06-09",
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
    return templates.TemplateResponse("show_artwork.html", {"request": request, "artwork": artwork_data})


@app.get("/put-artworks-form/{artwork_id}")
def update_artwork(request: Request, artwork_id: int):
    new_data = {
        "title": "string",
        "description": "string",
        "poster_url": "string",
        "release_date": "2023-06-09",
        "age_rating": "string",
        "star_rating": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}", json=new_data)
    updated_artwork = response.json()
    return templates.TemplateResponse("artwork_update.html", {"request": request, "artwork": updated_artwork})


@app.put("/put-artworks/{artwork_id}")
def update_artwork(request: Request, artwork_id: int):
    new_data = {
        "title": "string",
        "description": "string",
        "poster_url": "string",
        "release_date": "2023-06-09",
        "age_rating": "string",
        "star_rating": 0
    }
    response = requests.put(f"http://127.0.0.1:8000/artworks/{artwork_id}", json=new_data)
    updated_artwork = response.json()
    return templates.TemplateResponse("artwork_update.html", {"request": request, "artwork": updated_artwork})


@app.get("/get-artworks/{artwork_id}/comments")
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
    return templates.TemplateResponse("artwork_comment.html", {"request": request, "artwork": artwork_data})


@app.get("/get-artworks/{artwork_id}/reviews")
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
@app.get("/get-categories")
def show_categories(request: Request):
    category_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/categories", json=category_data)
    new_category = response.json()
    return templates.TemplateResponse("categories.html", {"request": request, "category": new_category})


@app.get("/post-categories-form")
def create_category(request: Request):
    category_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/categories", json=category_data)
    new_category = response.json()
    return templates.TemplateResponse("category_created.html", {"request": request, "category": new_category})


@app.post("/post-categories")
def create_category(request: Request):
    category_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.post("http://127.0.0.1:8000/categories", json=category_data)
    new_category = response.json()
    return templates.TemplateResponse("category_created.html", {"request": request, "category": new_category})


@app.get("/get-categories/{category_id}")
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


@app.get("/put-categories-form/{category_id}")
def update_category(request: Request, category_id: int):
    new_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get(f"http://127.0.0.1:8000/categories/{category_id}", json=new_data)
    updated_category = response.json()
    return templates.TemplateResponse("category_updated.html", {"request": request, "category": updated_category})


@app.put("/put-categories/{category_id}")
def update_category(request: Request, category_id: int):
    new_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.put(f"http://127.0.0.1:8000/categories/{category_id}", json=new_data)
    updated_category = response.json()
    return templates.TemplateResponse("category_updated.html", {"request": request, "category": updated_category})


# Route for comments
@app.post("/get-get-form-comments")
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


@app.get("/get-get-comments")
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


@app.get("/get-comments/{comment_id}")
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


@app.get("/put-comments-form/{comment_id}")
def update_comment(request: Request, comment_id: int):
    new_data = {
        "text": "string",
        "likes": 0,
        "dislikes": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/comments/{comment_id}", json=new_data)
    updated_comment = response.json()
    return templates.TemplateResponse("comment_update.html", {"request": request, "comment": updated_comment})


@app.put("/put-comments/{comment_id}")
def update_comment(request: Request, comment_id: int):
    new_data = {
        "text": "string",
        "likes": 0,
        "dislikes": 0
    }
    response = requests.put(f"http://127.0.0.1:8000/comments/{comment_id}", json=new_data)
    updated_comment = response.json()
    return templates.TemplateResponse("comment_update.html", {"request": request, "comment": updated_comment})


# Route for reviews
@app.get("/get-reviews")
def show_reviews(request: Request, review_data: dict):
    review_data = {
        "text": "string",
        "score": 0,
        "id": 0,
        "author_id": 0,
        "artwork_id": 0
    }
    response = requests.get("http://127.0.0.1:8000/reviews", json=review_data)
    new_review = response.json()
    return templates.TemplateResponse("reviews.html", {"request": request, "review": new_review})


@app.get("/get-reviews/{review_id}")
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
    return templates.TemplateResponse("review.html", {"request": request, "review": review_data})


@app.get("/put-reviews-form/{review_id}")
def update_review(request: Request, review_id: int):
    new_data = {
        "text": "string",
        "score": 0,
        "id": 0,
        "author_id": 0,
        "artwork_id": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/reviews/{review_id}", json=new_data)
    updated_review = response.json()
    return templates.TemplateResponse("review_update.html", {"request": request, "review": updated_review})


@app.put("/put-reviews/{review_id}")
def update_review(request: Request, review_id: int):
    new_data = {
        "text": "string",
        "score": 0,
        "id": 0,
        "author_id": 0,
        "artwork_id": 0
    }
    response = requests.put(f"http://127.0.0.1:8000/reviews/{review_id}", json=new_data)
    updated_review = response.json()
    return templates.TemplateResponse("review_update.html", {"request": request, "review": updated_review})


# Route for tags
@app.get("/get-tags/{tag_id}")
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


@app.get("/put-tags-form/{tag_id}")
def update_tag(request: Request, tag_id: int):
    new_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get(f"http://127.0.0.1:8000/tags/{tag_id}", json=new_data)
    updated_tag = response.json()
    return templates.TemplateResponse("tag_update.html", {"request": request, "tag": updated_tag})


@app.put("/put-tags/{tag_id}")
def update_tag(request: Request, tag_id: int):
    new_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.put(f"http://127.0.0.1:8000/tags/{tag_id}", json=new_data)
    updated_tag = response.json()
    return templates.TemplateResponse("tag_update.html", {"request": request, "tag": updated_tag})


@app.get("/get-tags")
def show_tags(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("tags.html", {"request": request, "tag": new_tag})


@app.get("/create-tag-form")
def create_tag(request: Request):
    tag_data = {
        "name": "",
        "description": ""
    }
    response = requests.get("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("tag_create.html", {"request": request, "tag": new_tag})


@app.post("/create-tag")
def create_tag(request: Request):
    tag_data = {
        "name": "string",
        "description": "string"
    }
    response = requests.post("http://127.0.0.1:8000/tags/", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("tag_create.html", {"request": request, "tag": new_tag})


# Route for users
@app.get("/get-users")
def show_users(request: Request):
    user_data = {
        "login": "string",
        "password": "string",
        "email": "user@example.com"
    }
    response = requests.get("http://127.0.0.1:8000/users/", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("users.html", {"request": request, "users": new_user})


@app.post("/make-users")
def create_user(request: Request):
    user_data = {
        "login": "string",
        "password": "string",
        "email": "user@example.com"
    }
    response = requests.post("http://127.0.0.1:8000/users/", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("user_create.html", {"request": request, "user": new_user})


@app.get("/get-users/{user_id}")
def show_user_one(request: Request, user_id: int):
    user_data = {
        "login": "string",
        "password": "string",
        "email": "user@example.com"
    }
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("user_show.html", {"request": request, "user": new_user})


@app.get("/put-users-form/{user_id}")
def update_user(request: Request, user_id: int):
    new_data = {
        "password": "string",
        "email": "user@example.com"
    }
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("update_user.html", {"request": request, "user": updated_user})


@app.put("/put-users/{user_id}")
def update_user(request: Request, user_id: int):
    new_data = {
        "password": "string",
        "email": "user@example.com"
    }
    response = requests.put(f"http://127.0.0.1:8000/users/{user_id}", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("update_user.html", {"request": request, "user": updated_user})


@app.get("/get-users/{user_id}/comments")
def show_user_comment(request: Request, user_id: int):
    user_data = {
        "text": "string",
        "likes": 0,
        "dislikes": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}/comments", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("show_user_comment.html", {"request": request, "user": new_user})


@app.get("/post-users-form/{user_id}/comments")
def create_user_comment(request: Request, user_id: int):
    new_data = {
        "text": "string",
        "likes": 0,
        "dislikes": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}/comments", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("create_user_comment.html", {"request": request, "user": updated_user})


@app.post("/post-users/{user_id}/comments")
def create_user_comment(request: Request, user_id: int):
    new_data = {
        "text": "string",
        "likes": 0,
        "dislikes": 0
    }
    response = requests.post(f"http://127.0.0.1:8000/users/{user_id}/comments", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("create_user_comment.html", {"request": request, "user": updated_user})


@app.get("/get-users/{user_id}/reviews")
def show_user_review(request: Request, user_id: int):
    user_data = {
        "text": "string",
        "score": 0
    }
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}/reviews", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("show_user_review.html", {"request": request, "user": new_user})


@app.post("/post-users/{user_id}/reviews")
def create_user_review(request: Request, user_id: int):
    new_data = {
        "text": "string",
        "score": 0
    }
    response = requests.post(f"http://127.0.0.1:8000/users/{user_id}/reviews", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("create_user_review.html", {"request": request, "user": updated_user})
