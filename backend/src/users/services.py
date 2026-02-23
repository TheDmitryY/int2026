from fastapi import Depends, HTTPException
from src.users.repository import UserRepository
from src.auth.schemas import CreateUserDTO
from src.users.schemas import ResponseUserDTO
from typing import List
import uuid


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_dto: CreateUserDTO) -> ResponseUserDTO:
        if await self.user_repo.get_by_email(user_dto.email):
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

        hashed_password = SecurityUtils.get_password_hash(user_dto.password)

        user_data = {
            "email": user_dto.email,
            "hashed_password": hashed_password,
            "role": "quest",
        }

        new_user = await self.user_repo.create(user_data)

        return new_user

    async def get_user_profile(self, user_id: uuid.UUID) -> ResponseUserDTO:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def delete_user(self, user_id: uuid.UUID) -> None:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self.user_repo.delete(user_id)
