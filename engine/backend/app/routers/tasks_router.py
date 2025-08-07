from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from engine.backend.app.database.connect_db import get_db
from engine.backend.app.services.tasks_service import get_all_tasks

router = APIRouter()

@router.get("/api/v1/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = get_all_tasks(db)
    return tasks


