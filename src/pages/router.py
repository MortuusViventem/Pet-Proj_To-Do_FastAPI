from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.auth.custom_auth import get_current_user
from src.routers import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc

from src.models import TasksOrm
from src.schemas import STask, STaskOwner

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/myTasks")
async def get_task_page(
        request: Request,
        db: AsyncSession = Depends(get_db),
        current_user: STaskOwner = Depends(get_current_user),
):
    query = select(TasksOrm).where(TasksOrm.owner_id == current_user.id).order_by(asc(TasksOrm.id))
    result = await db.execute(query)
    tasks = result.scalars().all()

    task_schemas = [STask.model_validate(task) for task in tasks]

    if current_user:
        user_authenticated = True
    else:
        user_authenticated = False

    return templates.TemplateResponse("tasks_page.html", {"request": request, "tasks": task_schemas, "user_authenticated": user_authenticated})


@router.get("/main")
async def get_base_page(
        request: Request,
):
    return templates.TemplateResponse("main.html", {"request": request})
