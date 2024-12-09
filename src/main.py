from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.routers import router as tasks_router
from src.pages.router import router as router_pages
from src.auth.router import router_auth as router_auth
from src.auth.router import router_users as router_users


app = FastAPI(
    title="Pet Proj ToDo",
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(tasks_router)
app.include_router(router_pages)
app.include_router(router_auth)
app.include_router(router_users)

origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

