from fastapi import Depends, HTTPException, APIRouter, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.auth.custom_auth import get_current_user
from src.database import async_session
from src.models import TasksOrm
from src.schemas import STaskOwner

router = APIRouter(
    prefix="/tasks",
    tags=["ToDo CRUD"],
)


templates = Jinja2Templates(directory="templates")


async def get_db():
    async with async_session() as session:
        yield session


@router.post("/add_task")
async def add_task(
        task_name: str = Form(...),
        description: str = Form(None),
        current_user: STaskOwner = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):

    actual_task = TasksOrm(
        task_name=task_name,
        description=description,
        owner_id=current_user.id,
    )
    db.add(actual_task)
    await db.commit()
    return RedirectResponse(url="/pages/myTasks", status_code=303)


@router.post("/update_status/{task_id}")
async def update_status(
        task_id: int,
        db: AsyncSession = Depends(get_db),
):

    result = await db.execute(select(TasksOrm).where(TasksOrm.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = not task.status
    db.add(task)
    await db.commit()

    return RedirectResponse(url="/pages/myTasks", status_code=303)


@router.post("/update_task/{task_id}")
async def update_task(
        task_id: int,
        task_name: str = Form(None),
        description: str = Form(None),
        db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(TasksOrm).where(TasksOrm.id == task_id))
    task = result.scalar_one_or_none()

    if task_name is not None:
        task.task_name = task_name
    if description is not None:
        task.description = description

    db.add(task)
    await db.commit()
    return RedirectResponse(url="/pages/myTasks", status_code=303)


@router.post("/delete/{task_id}")
async def delete(
        task_id: int,
        db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(TasksOrm).where(TasksOrm.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return RedirectResponse(url="/pages/myTasks", status_code=303)
