from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from database.config import get_async_session
from src.auth.models import User
from src.auth.services import AuthService
from src.users.repository import UserRepository
from jose import JWTError, jwt
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user_claims(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        user_id: str = payload.get("sub")
        role: str = payload.get("role")

        if user_id is None:
            raise credentials_exception

        return {"user_id": user_id, "role": role}

    except JWTError:
        raise credentials_exception


def role_required(role: str):
    async def role_checker(
        current_user: Annotated[User, Depends(get_current_user_claims)],
    ):
        if current_user.role != role:
            raise HTTPException(
                status_code=403, detail="Operation not permitted, insufficient role"
            )
        elif current_user.role != "user":
            raise HTTPException(status_code=401, detail="Not authenticated")
        return current_user

    return role_checker


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepository:
    return UserRepository(session)


async def get_auth_service(
    repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(repo)
