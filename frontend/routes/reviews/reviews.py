from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.dependencies import close_db_state, db_state, metadata
from backend.routers import reviews as reviews_router
app = FastAPI(
    on_startup=[lambda: metadata.create_all(bind=db_state.engine)],
    on_shutdown=[lambda: close_db_state(db_state)],
)
tags_metadata = [
    {
        "name": "crud - reviews",
        "description": "CRUD operations for REVIEWS table (data for reviews)."
    }
]

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

app.include_router(router=reviews_router.router, prefix="/reviews", tags=["crud - reviews"])
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

