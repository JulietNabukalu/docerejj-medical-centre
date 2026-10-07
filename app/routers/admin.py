from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import database, models
from .oauth2 import require_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def admin_dashboard(
    admin=Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    total_users = db.query(models.User).count()
    total_drugs = db.query(models.Drug).count()

    return {
        "message": "Welcome to the Admin Dashboard",
        "admin": admin.username,
        "total_users": total_users,
        "total_drugs": total_drugs
    }