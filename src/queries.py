# from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
# from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
# from sqlalchemy.exc import NoResultFound
#
# async def get_tasks(db: AsyncSession, user_id: int):
#     result = await db.execute(select(Task).filter(Task.owner_id == user_id))
#     return result.scalars().all()
#
# async def get_task(db: AsyncSession, task_id: int, user_id: int):
#     result = await db.execute(select(Task).filter(Task.id == task_id, Task.owner_id == user_id))
#     task = result.scalar_one_or_none()
#     if not task:
#         raise NoResultFound("Task not found")
#     return task
#
# async def create_task(db: AsyncSession, task_create: TaskCreate, user_id: int):
#     task = Task(**task_create.dict(), owner_id=user_id)
#     db.add(task)
#     await db.commit()
#     await db.refresh(task)
#     return task
#
# async def update_task(db: AsyncSession, task_id: int, user_id: int, task_update: TaskUpdate):
#     task = await get_task(db, task_id, user_id)
#     if task_update.title:
#         task.title = task_update.title
#     if task_update.description:
#         task.description = task_update.description
#     await db.commit()
#     await db.refresh(task)
#     return task
#
# async def delete_task(db: AsyncSession, task_id: int, user_id: int):
#     task = await get_task(db, task_id, user_id)
#     await db.delete(task)
#     await db.commit()
