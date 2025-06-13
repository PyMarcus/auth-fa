from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from core.configs import settings
from core.security import verify_password
from models import UserModel
from pydantic import EmailStr


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login"
)

async def auth(email: EmailStr, password: str, db: AsyncSession) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user



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
