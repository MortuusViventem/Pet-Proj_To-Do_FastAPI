from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, APIRouter, Form, Response, Request
from starlette import status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from .custom_auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from src.models import UsersOrm
from src.routers import get_db

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Users"],
)

templates = Jinja2Templates(directory="src/templates")


@router_auth.post("/register", status_code=201)
async def register_user(
        username: str = Form(...),
        password: str = Form(...),
        db: AsyncSession = Depends(get_db)
):

    query = select(UsersOrm).where(UsersOrm.username == username)
    result = await db.execute(query)
    existing_user = result.scalars().all()

    if existing_user:
        raise HTTPException(status_code=409, detail="Пользователь уже существует")

    hashed_password = get_password_hash(password)

    new_user = UsersOrm(
        username=username,
        password=hashed_password,
    )

    if not new_user:
        raise HTTPException(status_code=500, detail="Не удалось добавить запись")

    db.add(new_user)
    await db.commit()
    return RedirectResponse(url="/pages/main", status_code=303)


@router_auth.post("/login")
async def login_user(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
):
    user = await authenticate_user(username, password)
    access_token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse(url="/pages/myTasks", status_code=status.HTTP_302_FOUND)
    response.set_cookie("ToDo_access_token", access_token, httponly=True)
    return response


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("ToDo_access_token")
    return RedirectResponse(url="/pages/main", status_code=303)


@router_users.get("/me")
async def read_users_me(current_user: UsersOrm = Depends(get_current_user)):
    return current_user
