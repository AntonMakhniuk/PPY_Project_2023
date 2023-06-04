from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests

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
@app.get("/categories/{category_id}/artworks")
def show_artworks_inCategory(request: Request, artwork_data: dict,category_id: int):
    response = requests.get(f"http://127.0.0.1:8000/categories/{category_id}/artworks", json=artwork_data)
    new_artwork = response.json()
    return templates.TemplateResponse("show_artwork.html", {"request": request, "artwork": new_artwork})

@app.post("/categories/{category_id}/artworks")
def create_artworks_inCategory(request: Request, artwork_data: dict,category_id: int):
    response = requests.post(f"http://127.0.0.1:8000/categories/{category_id}/artworks", json=artwork_data)
    new_artwork = response.json()
    return templates.TemplateResponse("create_artwork.html", {"request": request, "artwork": new_artwork})

@app.get("/artworks")
def show_artwork(request: Request, artwork_data: dict):
    response = requests.get("http://127.0.0.1:8000/artworks", json=artwork_data)
    new_artwork = response.json()
    return templates.TemplateResponse("artworks.html", {"request": request, "artwork": new_artwork})

@app.get("/artworks/{artwork_id}")
def get_artwork(request: Request, artwork_id: int):
    response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}")
    artwork_data = response.json()
    return templates.TemplateResponse("show_artwork.html", {"request": request, "artwork": artwork_data})

@app.put("/artworks/{artwork_id}")
def update_artwork(request: Request, artwork_id: int, new_data: dict):
    response = requests.put(f"http://127.0.0.1:8000/artworks/{artwork_id}", json=new_data)
    updated_artwork = response.json()
    return templates.TemplateResponse("artwork_update.html", {"request": request, "artwork": updated_artwork})

@app.get("/artworks/{artwork_id}/comments")
def get_artwork_comments(request: Request, artwork_id: int):
    response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}/comments")
    artwork_data = response.json()
    return templates.TemplateResponse("artwork_comment.html", {"request": request, "artwork": artwork_data})

@app.get("/artworks/{artwork_id}/reviews")
def get_artwork_reviews(request: Request, artwork_id: int):
    response = requests.get(f"http://127.0.0.1:8000/artworks/{artwork_id}/reviews")
    artwork_data = response.json()
    return templates.TemplateResponse("artwork_review.html", {"request": request, "artwork": artwork_data})

# Route for categories
@app.post("/categories")
def show_categories(request: Request, category_data: dict):
    response = requests.post("http://127.0.0.1:8000/categories", json=category_data)
    new_category = response.json()
    return templates.TemplateResponse("categories.html", {"request": request, "category": new_category})

@app.post("/categories")
def create_category(request: Request, category_data: dict):
    response = requests.post("http://127.0.0.1:8000/categories", json=category_data)
    new_category = response.json()
    return templates.TemplateResponse("category_created.html", {"request": request, "category": new_category})

@app.get("/categories/{category_id}")
def get_category(request: Request, category_id: int):
    response = requests.get(f"http://127.0.0.1:8000/categories/{category_id}")
    category_data = response.json()
    return templates.TemplateResponse("category.html", {"request": request, "category": category_data})

@app.put("/categories/{category_id}")
def update_category(request: Request, category_id: int, new_data: dict):
    response = requests.put(f"http://127.0.0.1:8000/categories/{category_id}", json=new_data)
    updated_category = response.json()
    return templates.TemplateResponse("category_updated.html", {"request": request, "category": updated_category})


# Route for comments
@app.get("/comments")
def create_comment(request: Request, comment_data: dict):
    response = requests.get("http://127.0.0.1:8000/comments", json=comment_data)
    new_comment = response.json()
    return templates.TemplateResponse("comment_create.html", {"request": request, "comment": new_comment})

@app.get("/comments/{comment_id}")
def get_comment(request: Request, comment_id: int):
    response = requests.get(f"http://127.0.0.1:8000/comments/{comment_id}")
    comment_data = response.json()
    return templates.TemplateResponse("comment.html", {"request": request, "comment": comment_data})

@app.put("/comments/{comment_id}")
def update_comment(request: Request, comment_id: int, new_data: dict):
    response = requests.put(f"http://127.0.0.1:8000/comments/{comment_id}", json=new_data)
    updated_comment = response.json()
    return templates.TemplateResponse("comment_update.html", {"request": request, "comment": updated_comment})

# Route for reviews
@app.post("/reviews")
def create_review(request: Request, review_data: dict):
    response = requests.post("http://127.0.0.1:8000/reviews", json=review_data)
    new_review = response.json()
    return templates.TemplateResponse("review_create.html", {"request": request, "review": new_review})

@app.get("/reviews/{review_id}")
def get_review(request: Request, review_id: int):
    response = requests.get(f"http://127.0.0.1:8000/reviews/{review_id}")
    review_data = response.json()
    return templates.TemplateResponse("review.html", {"request": request, "review": review_data})

@app.put("/reviews/{review_id}")
def update_review(request: Request, review_id: int, new_data: dict):
    response = requests.put(f"http://127.0.0.1:8000/reviews/{review_id}", json=new_data)
    updated_review = response.json()
    return templates.TemplateResponse("review_update.html", {"request": request, "review": updated_review})



# Route for tags
@app.get("/tags/{tag_id}")
def get_tag(request: Request, tag_id: int):
    response = requests.get(f"http://127.0.0.1:8000/tags/{tag_id}")
    tag_data = response.json()
    return templates.TemplateResponse("tag.html", {"request": request, "tag": tag_data})

@app.put("/tags/{tag_id}")
def update_tag(request: Request, tag_id: int, new_data: dict):
    response = requests.put(f"http://127.0.0.1:8000/tags/{tag_id}", json=new_data)
    updated_tag = response.json()
    return templates.TemplateResponse("tag_update.html", {"request": request, "tag": updated_tag})

@app.get("/tags")
def show_tags(request: Request, tag_data: dict):
    response = requests.get("http://127.0.0.1:8000/tags", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("tags.html", {"request": request, "tag": new_tag})

@app.post("/createtag")
def create_tag(request: Request, tag_data: dict):
    response = requests.post("http://127.0.0.1:8000/tags", json=tag_data)
    new_tag = response.json()
    return templates.TemplateResponse("tag_create.html", {"request": request, "tag": new_tag})


# Route for users
@app.get("/users")
def show_users(request: Request, user_data: dict):
    response = requests.get("http://127.0.0.1:8000/users/", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("users.html", {"request": request, "user": new_user})

@app.post("/users")
def create_user(request: Request, user_data: dict):
    response = requests.post("http://127.0.0.1:8000/users/", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("user_create.html", {"request": request, "user": new_user})

@app.get("/users/{user_id}")
def show_user(request: Request, user_id: int,user_data: dict):
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("user_added.html", {"request": request, "user": new_user})

@app.put("/users/{user_id}")
def update_user(request: Request, user_id: int, new_data: dict):
    response = requests.put(f"http://127.0.0.1:8000/users/{user_id}", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("update_user.html", {"request": request, "user": updated_user})

@app.get("/users/{user_id}/comments")
def show_user_comment(request: Request, user_id: int,user_data: dict):
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}/comments", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("show_user_comment.html", {"request": request, "user": new_user})

@app.post("/users/{user_id}/comments")
def create_user_comment(request: Request, user_id: int, new_data: dict):
    response = requests.post(f"http://127.0.0.1:8000/users/{user_id}/comments", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("create_user_comment.html", {"request": request, "user": updated_user})

@app.get("/users/{user_id}/reviews")
def show_user_review(request: Request, user_id: int,user_data: dict):
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}/reviews", json=user_data)
    new_user = response.json()
    return templates.TemplateResponse("show_user_review.html", {"request": request, "user": new_user})

@app.post("/users/{user_id}/reviews")
def create_user_review(request: Request, user_id: int, new_data: dict):
    response = requests.post(f"http://127.0.0.1:8000/users/{user_id}/reviews", json=new_data)
    updated_user = response.json()
    return templates.TemplateResponse("create_user_review.html", {"request": request, "user": updated_user})

