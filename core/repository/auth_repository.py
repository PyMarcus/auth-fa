from typing import Optional, List
from sqlalchemy.future import select
from core.security import verify_password
from models import UserModel
from pydantic import EmailStr



class AuthRepository:
    def __init__(self, db) -> None:
        self.__db = db

    async def get_user(self, email: EmailStr, password: str) -> Optional[UserModel]:
        async with self.__db as session:
            query = select(UserModel).filter(UserModel.email == email)
            result = await session.execute(query)
            user: UserModel = result.scalars().unique().one_or_none()

            if not user:
                return None

            if not verify_password(password, user.password):
                return None

            return user

    async def get_user_by_id(self, id: int) -> Optional[UserModel]:
        async with self.__db as session:
            query = select(UserModel).filter(UserModel.id == id)
            result = await session.execute(query)
            user: UserModel = result.scalars().unique().one_or_none()

            if not user:
                return None

            return user

    async def get_all_user(self) -> List[UserModel]:
        async with self.__db as session:
            query = select(UserModel)
            result = await session.execute(query)
            users = result.scalars().all()

            return users

    async def create(self, user: UserModel) -> bool:
        try:
            async with self.__db as session:
                session.add(user)
                await session.commit()
                return True
        except Exception as e:
            print(e)
            return False
