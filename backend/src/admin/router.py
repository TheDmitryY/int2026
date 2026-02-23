from src.admin.dependencies import get_admin_service
from src.admin.services import AdminService
from src.auth.dependencies import role_required
from src.users.schemas import ResponseUserDTO
from src.auth.models import User
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated
import uuid
import datetime

router = APIRouter()


@router.get("/")
async def get(limit: int, skip: int):
    pass


@router.post("/")
async def create_order_directly(
    latitude: str, longitude: str, subtotal: int, timestamp: str
):
    pass


@router.post("/import")
async def import_csv(file: bytes):
    pass
