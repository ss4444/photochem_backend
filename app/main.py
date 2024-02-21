from app.api.auth import router as auth_router
from app.api.admin import router as admin_router
from app.api.user import router as user_router
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import app.api.auth
from app.core.db import database

# DB_URL = "postgresql://meta_db_user:meta_db_password@localhost:5432/db"


# database = databases.Database(DB_URL)


app = FastAPI()

app = FastAPI()

app.state.database = database

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    database_= app.state.database
    if not database_.is_connected:
        await database.connect()

@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database.disconnect()


app.include_router(auth_router, tags=["Auth"])
app.include_router(admin_router, tags=["Admin"])
app.include_router(user_router, tags=["User"])
