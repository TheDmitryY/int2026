from src.admin.repository import AdminRepository
from src.admin.exceptions import NotFoundException, BanException, UnBanException
from src.users.schemas import ResponseUserDTO
from fastapi import Depends
import uuid
from typing import List


class AdminService:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    async def get_users(self, skip: int, limit: int) -> List[ResponseUserDTO]:
        users = await self.admin_repo.get_all(skip=skip, limit=limit)
        if not users:
            raise NotFoundException("Users not found")
        return users

    async def get_user(self, user_id: uuid.UUID) -> ResponseUserDTO:
        users = await self.admin_repo.get_by_id(user_id=user_id)
        if not users:
            raise NotFoundException(f"User with id: {user_id} not found")
        return users

    async def ban_user(self, user_id: uuid.UUID) -> ResponseUserDTO:
        users = await self.admin_repo.get_by_id(user_id=user_id)
        if not users:
            raise NotFoundException(f"User with id: {user_id} not found")
        ban = await self.admin_repo.ban_user(user_id=user_id)
        return ban

    async def unban_user(self, user_id: uuid.UUID) -> ResponseUserDTO:
        users = await self.admin_repo.get_by_id(user_id=user_id)
        if not users:
            raise NotFoundException(f"User with id: {user_id} not found")
        unban = await self.admin_repo.unban_user(user_id=user_id)
        return unban

    async def get_all_banned_users(
        self, skip: int, limit: int
    ) -> List[ResponseUserDTO]:
        return await self.admin_repo.get_banned_users(skip=skip, limit=limit)

    async def get_banned_user(self, user_id: uuid.UUID) -> ResponseUserDTO:
        banned_user = await self.admin_repo.get_banned_user(user_id=user_id)
        if not banned_user:
            raise BanException("Users not found")
        return banned_user

    async def ban_user_by_email(self, email: str) -> ResponseUserDTO:
        users = await self.admin_repo.ban_user_by_email(email=email)
        if not users:
            raise BanException("Users not found")
        return users
