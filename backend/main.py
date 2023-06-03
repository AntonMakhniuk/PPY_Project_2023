from fastapi import FastAPI

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
app.include_router(router=tags_router.router, prefix="/tags")
app.include_router(router=categories_router.router, prefix="/categories")
app.include_router(router=artworks_router.router, prefix="/artworks")
app.include_router(router=comments_router.router, prefix="/comments")
app.include_router(router=reviews_router.router, prefix="/reviews")
app.include_router(router=users_router.router, prefix="/users")


@app.get("/")
def root():
    return {"message": "Hello World"}
