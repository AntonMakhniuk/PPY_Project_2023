from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
from fastapi.staticfiles import StaticFiles

from backend.dependencies import close_db_state, db_state, metadata
from backend.routers import artworks as artworks_router

app = FastAPI(
    on_startup=[lambda: metadata.create_all(bind=db_state.engine)],
    on_shutdown=[lambda: close_db_state(db_state)],
)
tags_metadata = [
    {
        "name": "crud - artworks",
        "description": "CRUD operations for ARTWORK table (data for artworks)."
    }
]

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

app.include_router(router=artworks_router.router, prefix="/artworks", tags=["crud - artworks"])


# @app.get("/get-artworks", response_class=HTMLResponse)
# def get_artworks(request: Request, skip: int = 0, limit: int = 100)->HTMLResponse:
#     response = requests.get(f"http://127.0.0.1:8000/artworks/?skip={skip}&limit={limit}")
#     artworks = response.json()
#     return templates.TemplateResponse("artworks.html", {"request": request, "artworks": artworks})
#
#
# @app.get("/get-artwork/{artwork_id}")
# def get_artwork(request: Request, artwork_id: int):
#     response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}")
#     artwork = response.json()
#     return templates.TemplateResponse("artwork.html", {"request": request, "artwork": artwork})
#
#
# @app.put("/update-artwork/{artwork_id}")
# def update_artwork(request: Request, artwork_id: int, artwork_schema_updated: dict):
#     response = requests.put(f"http://127.0.0.1:8000/artworks/{artwork_id}", json=artwork_schema_updated)
#     updated_artwork = response.json()
#     return templates.TemplateResponse("updated_artwork.html", {"request": request, "artwork": updated_artwork})
#
#
# @app.delete("/delete-artwork/{artwork_id}")
# def delete_artwork(request: Request, artwork_id: int):
#     response = requests.delete(f"http://127.0.0.1:8000/artworks/{artwork_id}")
#     deleted_artwork = response.json()
#     return templates.TemplateResponse("deleted_artwork.html", {"request": request, "artwork": deleted_artwork})
#
#
# @app.get("/get-comments/{artwork_id}")
# def get_comments(request: Request, artwork_id: int, skip: int = 0, limit: int = 100):
#     response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}/comments/?skip={skip}&limit={limit}")
#     comments = response.json()
#     return templates.TemplateResponse("comments.html", {"request": request, "comments": comments})
#
#
# @app.get("/get-reviews/{artwork_id}")
# def get_reviews(request: Request, artwork_id: int, skip: int = 0, limit: int = 100):
#     response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}/reviews/?skip={skip}&limit={limit}")
#     reviews = response.json()
#     return templates.TemplateResponse("reviews.html", {"request": request, "reviews": reviews})
#
#
# @app.get("/get-tags/{artwork_id}")
# def get_tags(request: Request, artwork_id: int, skip: int = 0, limit: int = 100):
#     response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}/tags/?skip={skip}&limit={limit}")
#     tags = response.json()
#     return templates.TemplateResponse("tags.html", {"request": request, "tags": tags})
#
#
# @app.post("/add-tag/{artwork_id}/{tag_id}")
# def add_tag(request: Request, artwork_id: int, tag_id: int):
#     response = requests.post(f"http://127.0.0.1:8000/artworks/{artwork_id}/tags/{tag_id}")
#     updated_artwork = response.json()
#     return templates.TemplateResponse("updated_artwork.html", {"request": request, "artwork": updated_artwork})
#
#
# @app.delete("/remove-tag/{artwork_id}/{tag_id}")
# def remove_tag(request: Request, artwork_id: int, tag_id: int):
#     response = requests.delete(f"http://127.0.0.1:8000/artworks/{artwork_id}/tags/{tag_id}")
#     updated_artwork = response.json()
#     return templates.TemplateResponse("updated_artwork.html", {"request": request, "artwork": updated_artwork})
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


@app.get("/get-artworks/{artwork_id}/tags")
def get_tags_in_artwork(request: Request, artwork_id: int):
    artwork_data = {
        "name": "string",
        "description": "string",
        "id": 0,
        "artworks": [
            {
                "title": "string",
                "description": "string",
                "poster_url": "string",
                "release_date": "2023-06-18",
                "age_rating": "string",
                "star_rating": 0
            }
        ]
    }
    response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}/tags", json=artwork_data)
    new_artwork = response.json()
    return templates.TemplateResponse("artworks-single.html", {"request": request, "artwork": new_artwork})


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


@app.delete("/remove-tag/{artwork_id}/{tag_id}")
def remove_tag(request: Request, artwork_id: int, tag_id: int):
    response = requests.delete(f"http://127.0.0.1:8000/artworks/{artwork_id}/tags/{tag_id}")
    updated_artwork = response.json()
    return templates.TemplateResponse("updated_artwork.html", {"request": request, "artwork": updated_artwork})
