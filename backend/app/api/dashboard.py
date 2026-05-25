"""
Stubs for dashboard, reports and hardware endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import get_current_user

router = APIRouter()

@router.get("/")
async def get_dashboard(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get dashboard summary data."""
    return {
        "status": "ok",
        "message": "Dashboard stub endpoint"
    }
