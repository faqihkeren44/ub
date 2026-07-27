from fastapi import APIRouter, Depends
from ..auth import verify_admin

from . import dashboard
from . import members

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_admin)]
)

router.include_router(dashboard.router)
router.include_router(members.router)