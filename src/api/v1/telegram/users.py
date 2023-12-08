from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException

from src.services.telegram.user import (
    get_cache_detail
)

router = APIRouter()


@router.get('/_cache_details', include_in_schema=True)
async def user_cache_details():
    # return get_cache_detail()
    raise NotImplementedError