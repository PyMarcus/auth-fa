from sqlalchemy import Column, Integer, String, Boolean

from core.configs import settings


class UserModel(settings.DBBaseModel):
    __tablename__: str = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(256), nullable=False)
    email: str = Column(String(256), index=True, nullable=False, unique=True)
    password: str = Column(String(500), nullable=False)
    admin: bool = Column(Boolean, default=False)
