from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app import database, models
from ..auth import verify_admin

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    db: Session = Depends(database.get_db),
    msg: str = None,
    admin: models.Admin = Depends(verify_admin)
):
    message = ""

    all_members = db.query(models.Member)

    registers = (
        all_members
        .filter(models.Member.member_status == models.MemberStatus.PENDING)
        .order_by(models.Member.submitted_at.desc())
        .limit(5)
        .all()
    )

    year = datetime.now().year
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)

    active_members = (
        all_members
        .filter(models.Member.member_status == models.MemberStatus.ACTIVE)
        .filter(
            models.Member.approved_at >= start,
            models.Member.approved_at < end
        )
    )

    total_all_members = all_members.count()
    total_active_members = active_members.count()
    total_inactive_members = (
        all_members
        .filter(models.Member.member_status != models.MemberStatus.ACTIVE)
        .count()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "admin": admin,
            "all_members": all_members,
            "registers": registers,
            "active_members": active_members,
            "total_all": total_all_members,
            "total_active": total_active_members,
            "total_inactive": total_inactive_members
        }
    )