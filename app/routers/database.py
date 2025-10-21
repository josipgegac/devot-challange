from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.seed_data import rebuild_database

router = APIRouter(prefix="/rebuild_database", tags=["database"])

@router.post("")
def create_new_database(db: Session = Depends(get_db)):
    rebuild_database(db)
    return {"status": "database created"}
