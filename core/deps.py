from typing import Optional, Any, AsyncGenerator
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from core.auth import oauth2_schema
from core.configs import settings
from core.db import Session
from core.repository import AuthRepository
from models import UserModel


class TokenData(BaseModel):
    username: Optional[Any] = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()


def get_auth_repository(session: AsyncSession = Depends(get_session)) -> AuthRepository:
    return AuthRepository(session)


async def get_current_user(token: str = Depends(oauth2_schema), auth_repository: AuthRepository = Depends(get_auth_repository)) -> UserModel:
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITH],
            options={"verify_aud": False}
        )
        username: str = payload.get("sub")
        if not username:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = await auth_repository.get_user_by_id(int(token_data.username))
    if not user:
        raise credential_exception
    return user
