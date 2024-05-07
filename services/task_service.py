import time 

from asyncmy.errors import DatabaseError
from fastapi import HTTPException, status
from sqlalchemy import select, and_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from services.rc_db_Service import RCDBService
from model.db.task import Task
from model.dto.task_dto import CreateTask, StatusType, UpdateTask
from utils import uuid_generator, timestamp_convertor


class TaskService(RCDBService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.session = session
        now = time.time()
        self.created_at = int(now)
        self.updated_at = int(now)
        
    async def create_task(self, user_id, task: CreateTask):
        try:
            task_id = uuid_generator.get_uuid()
            
            due_date_timestamp = timestamp_convertor.iso8601_to_unix_timestamp(str(task.due_date))
        
            if due_date_timestamp <= time.time():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reminder")
            
            task = Task(
                task_id = task_id,
                user_id = user_id,
                title = task.title,
                due_date = due_date_timestamp,
                priority = task.priority,
                status = StatusType.pending,
                created_at = self.created_at,
                updated_at = self.updated_at
            )
            
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)
            
            return task
        except DatabaseError as db_error:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(db_error)}")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")
        
    async def get_tasks(self, user_id):
        try:
            
            query = (
                select(
                    Task.task_id,
                    Task.title,
                    Task.due_date,
                    Task.status,
                    Task.priority
                )
                .where(Task.user_id == user_id)
            )
            
            query_result = await self.session.execute(query)
            
            return [result._asdict() for result in query_result]
        
        except DatabaseError as db_error:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(db_error)}")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")
        
        
    async def update_task(self, task: UpdateTask):
        try:
            updated_task_data = {Task.updated_at: self.updated_at}
            
            # adding timestamp to dictionary if present
            if task.due_date:
                due_date_timestamp = timestamp_convertor.iso8601_to_unix_timestamp(str(task.due_date))
                if due_date_timestamp <= time.time():
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reminder")
                updated_task_data[Task.due_date] = due_date_timestamp
    
            
            # adding other attributes into dictionay if present
            attributes = ['title', 'priority']
            
            for attr in attributes:
                value = getattr(task, attr)
                if value is not None:
                    updated_task_data[getattr(Task, attr)] = value
                    
            query = (
                update(Task)
                .where(Task.task_id == task.task_id)
                .values(updated_task_data)
            )
            
            query_result = await self.session.execute(query)
            await self.session.commit()
            
            return query_result
        
        except DatabaseError as db_error:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(db_error)}")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")
        
    
        
    async def delete_tasks(self, task_id):
        try:
            
            query = (
                delete(Task)
                .where(Task.task_id == task_id)
            )
            
            query_result = await self.session.execute(query)
            await self.session.commit()
            
            return query_result
        
        except DatabaseError as db_error:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(db_error)}")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")
        
    async def change_task_status(self, task_id):
        try:
            
            async with self.session.begin():
                query = (
                    select(Task.status)
                    .where(Task.task_id == task_id)
                )
                
                status = (await self.session.execute(query)).scalars().one()
                
                updated_status = ''
                
                if status == 'pending':
                    updated_status = 'completed'
                else:
                    updated_status = 'pending'
                    
                query = (
                    update(Task)
                    .where(Task.task_id == task_id)
                    .values({Task.status: updated_status})
                )

                query_result = await self.session.execute(query)
            return query_result
        except DatabaseError as db_error:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(db_error)}")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")
    
    
        
        