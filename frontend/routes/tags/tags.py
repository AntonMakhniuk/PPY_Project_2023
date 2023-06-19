from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
from fastapi.staticfiles import StaticFiles

from backend.dependencies import close_db_state, db_state, metadata
from backend.routers import tags as tags_router

app = FastAPI(
    on_startup=[lambda: metadata.create_all(bind=db_state.engine)],
    on_shutdown=[lambda: close_db_state(db_state)],
)
tags_metadata = [
    {
        "name": "crud - tags",
        "description": "CRUD operations for TAG table (data for tags)."
    }
]

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

app.include_router(router=tags_router.router, prefix="/tags", tags=["crud - tags"])

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

