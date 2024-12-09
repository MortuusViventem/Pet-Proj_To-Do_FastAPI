from datetime import timedelta, datetime

from jose import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request
from passlib.context import CryptContext
from sqlalchemy import select

from src.config import settings
from src.database import async_session
from src.models import UsersOrm

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


async def authenticate_user(
        username: str,
        password: str,
):
    async with (async_session() as session):
        result = await session.execute(
            select(UsersOrm).where(UsersOrm.username == username)
        )
        user = result.scalars().first()

        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user


def get_token(request: Request):
    token = request.cookies.get("ToDo_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Токен отсутствует")
    return token


async def get_current_user(token: str = Depends(get_token)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    except InvalidTokenError:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if not user_id:
        raise credentials_exception

    async with async_session() as session:
        result = await session.execute(
            select(UsersOrm).where(UsersOrm.id == int(user_id))
        )
        user = result.scalars().first()
        if user is None:
            raise credentials_exception
        return user

