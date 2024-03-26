from fastapi import APIRouter, Depends, HTTPException, Response
import jwt
from app.managers.users import authenticate_user, get_user_current
from app.models import User
import asyncpg
from app.schemas import (
    UserAllInfo,
    UserGet,
    UserAuth,
    UserEdit,
    CheckEmail,
    CheckAnswer,
    UserReg,
)
from passlib.hash import bcrypt
import ormar

from app.settings import settings

router = APIRouter(prefix="")


@router.post("/")
async def auth(data: UserAuth):
    try:
        user = await authenticate_user(data.username, data.password)
        if not user:
            return Response(status_code=404, content={"error": "invaid credentials"})
        user = UserGet(id=str(user.id), username=user.username, password=user.password)
        token = jwt.encode(user.dict(), settings.secret_key)
        return {"access_token": token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=404, detail="Invalid")


@router.post("/reg")
async def register(data_user: UserReg):
    if data_user.secret_code == settings.secret_code:
        is_admin = True
    elif data_user.secret_code == "123":
        is_admin = False
    else:
        raise HTTPException(status_code=403, detail="Invalid code")
    try:
        user = UserAllInfo(
            last_name=data_user.last_name,
            name=data_user.name,
            username=data_user.username,
            password=data_user.password,
            is_admin=is_admin
        )
        user.password = bcrypt.hash(user.password)
        user_dict = user.dict()
        await User.objects.create(**user_dict)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="User already exists")
    return Response(status_code=200, content="User created")


@router.post("/check_username")
async def check_username(username: CheckEmail):
    try:
        await User.objects.get(username=username.username)
        return CheckAnswer(answer=False)
    except ormar.exceptions.NoMatch:
        return CheckAnswer(answer=True)


@router.patch("/me")
async def user_edit(new_user: UserEdit, user=Depends(get_user_current)):
    if new_user.password:
        new_user.password = bcrypt.hash(new_user.password)
    user = await User.objects.get(id=user.id)
    try:
        await user.update(**{k: v for k, v in new_user.dict().items() if v})
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail="Nickname is already in use")
    return user


@router.get("/me")
async def get_me(user=Depends(get_user_current)):
    user_get = await User.objects.get(id=user.id)
    return user_get


@router.get("/is_admin")
async def is_admin(user=Depends(get_user_current)):
    if user.is_admin:
        return CheckAnswer(answer=True)
    else:
        return CheckAnswer(answer=False)
