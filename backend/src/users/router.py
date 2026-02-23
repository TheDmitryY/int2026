from fastapi import APIRouter, Depends, HTTPException

from src.users.services import UserService
from src.users.dependencies import get_user_service
from src.users.schemas import ResponseUserDTO
from typing import List

router = APIRouter()
