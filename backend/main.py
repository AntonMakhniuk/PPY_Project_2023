from fastapi import FastAPI

from backend.dependencies import close_connection, engine, metadata
from backend.routers import tags as tags_router
from backend.routers import categories as categories_router

app = FastAPI(
    on_startup=[lambda: metadata.create_all(bind=engine)],
    on_shutdown=[lambda: close_connection()],
)
app.include_router(router=tags_router.router, prefix="/tags")
app.include_router(router=categories_router.router, prefix="/categories")


@app.get("/")
def root():
    return {"message": "Hello World"}
