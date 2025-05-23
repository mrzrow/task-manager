from fastapi import APIRouter
from .v1.user import router as user_router


router_v1 = APIRouter(prefix="/v1")
router_v1.include_router(user_router)
