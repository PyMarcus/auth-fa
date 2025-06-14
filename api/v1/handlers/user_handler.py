from typing import List

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from core.auth import auth, create_access_token
from core.deps import get_auth_repository, get_current_user
from core.repository import AuthRepository
from core.security import create_hash
from models import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaRequest, UserSchemaLogin

router = APIRouter()


@router.post("/login")
async def login(data: UserSchemaLogin, auth_repository: AuthRepository = Depends(get_auth_repository)):
    user = await auth(email=data.email, password=data.password, auth_repository=auth_repository)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect credentials")
    return JSONResponse(
        content={"access_token": create_access_token(sub=str(user.id)), "token_type": "bearer"},
        status_code=status.HTTP_200_OK
    )


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_user(user: UserSchemaRequest, auth_repository: AuthRepository = Depends(get_auth_repository)):
    new_user: UserModel = UserModel(
        name=user.name,
        email=user.email,
        password=create_hash(user.password),
        admin=user.admin
    )

    if await auth_repository.create(new_user):
        return UserSchemaBase.from_orm(new_user)

    raise HTTPException(detail="Fail to create user", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/", response_model=List[UserSchemaBase])
async def list_all_users(auth_repository: AuthRepository = Depends(get_auth_repository), current_user: UserModel = Depends(get_current_user)):
    users = await auth_repository.get_all_user()
    if users:
        return [UserSchemaBase.from_orm(user) for user in users]

    raise HTTPException(detail="No users data", status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{user_id}", response_model=UserSchemaBase)
async def get_user_by_id(user_id: int, auth_repository: AuthRepository = Depends(get_auth_repository)):
    user = await auth_repository.get_user_by_id(user_id)
    if user:
        return UserSchemaBase.from_orm(user)

    raise HTTPException(detail="No user data", status_code=status.HTTP_204_NO_CONTENT)
