import ormar

from app.models import User

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from uuid import UUID
from app.settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(username: str, password: str):
    try:
        user = await User.objects.get(username=username)
        if not user.verify_password(password):
            return False
        return user
    except ormar.NoMatch:
        return False


async def get_user_current(token: str = Depends(oauth2_scheme)):
    # try:
    payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    user = await User.objects.get(id=UUID(payload["id"]))
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
    return user
