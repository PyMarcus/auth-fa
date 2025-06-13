from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import EmailStr
from pytz import timezone
from core.configs import settings
from core.repository import AuthRepository
from models import UserModel

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login"
)

async def auth(email: EmailStr, password: str, auth_repository: AuthRepository) -> Optional[UserModel]:
    return await auth_repository.get_user(email, password)



def create_access_token(sub: str) -> str:
    return _create_token(
        token_type="access_token",
        time_to_live=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )


def _create_token(token_type: str, time_to_live: timedelta, sub: str) -> str:
    sp = timezone("AMERICA/Sao_Paulo")
    expire = datetime.now(tz=sp) + time_to_live

    payload = {
        "type": token_type,
        "exp": expire,
        "iat": datetime.now(tz=sp),
        "sub": str(sub)
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITH)
