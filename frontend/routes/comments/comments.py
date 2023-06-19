from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
from fastapi.staticfiles import StaticFiles

from backend.dependencies import close_db_state, db_state, metadata
from backend.routers import comments as comments_router

app = FastAPI(
    on_startup=[lambda: metadata.create_all(bind=db_state.engine)],
    on_shutdown=[lambda: close_db_state(db_state)],
)
tags_metadata = [
    {
        "name": "crud - comments",
        "description": "CRUD operations for COMMENT table (data for comments)."
    }
]

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

app.include_router(router=comments_router.router, prefix="/comments", tags=["crud - comments"])
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
