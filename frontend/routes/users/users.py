from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.dependencies import close_db_state, db_state, metadata
from backend.routers import users as users_router
app = FastAPI(
    on_startup=[lambda: metadata.create_all(bind=db_state.engine)],
    on_shutdown=[lambda: close_db_state(db_state)],
)
tags_metadata = [
    {
        "name": "crud - users",
        "description": "CRUD operations for USER table (data for users)."
    }
]

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

app.include_router(router=users_router.router, prefix="/users", tags=["crud - users"])

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
