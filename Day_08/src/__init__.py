"""
Main FastAPI app initializer.
Runs DB initialization on startup (init_db) via the lifespan context manager.
"""

from fastapi import FastAPI
from src.auth.routes import auth_router
from src.books.routes import router
from contextlib import asynccontextmanager
from src.db.main import init_db

# Lifespan context manager — run startup/shutdown tasks here
@asynccontextmanager
async def life_span(app: FastAPI):
    print("🚀 The server is starting ...")
    # Initialize database tables (create_all)
    await init_db()

    # (Optional) you could run seed/test data here if you want — commented out:
    # from src.db.seed import seed_data
    # await seed_data()

    yield
    print("🛑 The server has stopped ...")


version = "v1"

app = FastAPI(
    title="📚 Bookly API",
    description="A REST API for managing book reviews using FastAPI + SQLModel",
    version=version,
    lifespan=life_span
)

# Attach books router under /api/v1/book
app.include_router(router, prefix=f"/api/{version}/book", tags=["book"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])