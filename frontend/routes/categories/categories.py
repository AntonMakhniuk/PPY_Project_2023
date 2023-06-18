from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
from starlette.staticfiles import StaticFiles

from backend.dependencies import close_db_state, db_state, metadata
from backend.routers import categories as categories_router

app = FastAPI(
    on_startup=[lambda: metadata.create_all(bind=db_state.engine)],
    on_shutdown=[lambda: close_db_state(db_state)],
)
tags_metadata = [
    {
        "name": "crud - categories",
        "description": "CRUD operations for CATEGORY table (data for categories)."
    }
]
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")
app.include_router(router=categories_router.router, prefix="/categories", tags=["crud - categories"])

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


@app.delete("/remove-tag/{category_id}")
def remove_category(request: Request, category_id: int):
    response = requests.delete(f"http://127.0.0.1:8000/artworks/{category_id}")
    updated_category = response.json()
    return templates.TemplateResponse("category.html", {"request": request, "artwork": updated_category})

