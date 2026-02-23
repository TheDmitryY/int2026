from src.users.repository import UserRepository
from src.auth.exceptions import BusinessRuleException
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from src.users.schemas import UserEntity
from src.auth.schemas import CreateUserDTO, TokenDTO, LoginUserDTO, AuthResultDTO
from src.users.schemas import ResponseUserDTO
from src.auth.utils import ArgonPasswordHasher, JwtTokenService
from fastapi import HTTPException
import uuid


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: ArgonPasswordHasher,
        token_service: JwtTokenService,
    ):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def register_user(self, user_dto: CreateUserDTO) -> str:
        user = await self.user_repo.get_by_email(email=user_dto.email)
        if user:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

        hashed_password = self.password_hasher.hash(user_dto.password)

        new_user = UserEntity(
            id=None,  # Let the database auto-generate the UUID
            email=user_dto.email,
            hashed_password=hashed_password,
            username=user_dto.username,
            role="quest",
        )

        saved_user = await self.user_repo.create(new_user)
        return saved_user

    async def login_user(
        self, email: str, password: str
    ) -> str:  # Return string instead of TokenDTO
        user = await self.user_repo.get_by_email_with_password(email=email)
        if not user:
            raise HTTPException(status_code=409, detail="Invalid credentials")
        if not self.password_hasher.verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = self.token_service.create_access_token(user_id=user.id, role="quest")
        return token

    async def logout_user(response: Response):
        response.delete_cookie(
            key=COOKIE_KEY, httponly=True, secure=True, samesite="lax"
        )
        return {"message": "Logged out"}
