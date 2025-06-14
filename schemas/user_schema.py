from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    admin: bool

    model_config = {
        "from_attributes": True
    }


class UserSchemaRequest(UserSchemaBase):
    password: str


class UserSchemaUpdate(UserSchemaBase):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    admin: Optional[bool]


class UserSchemaLogin(BaseModel):
    email: EmailStr
    password: str
