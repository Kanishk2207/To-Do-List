import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import AuthValidator
from internal.database.mysql import get_db
from utils.token_generator import __user_model
from model.dto.task_dto import CreateTask as CreateTaskDto
from model.dto.task_dto import UpdateTask as UpdateTaskDto
from model.dto.task_dto import TaskId as TaskIdDto
from services import task_service

router = APIRouter()

@router.post('/task', dependencies=[Depends(AuthValidator())], tags=['task'])
async def create_tasks( request: CreateTaskDto,
                       jwt_token: str = Depends(AuthValidator()),
                       mysql_session: AsyncSession = Depends(get_db),
):
    try:
        task_srv = task_service.TaskService(mysql_session)
        
        user = __user_model(jwt_token)
        user_id = user.get('user_id')
        
        task = await task_srv.create_task(user_id, request)
        
        return {
            "message": "Task added successfully"
        }
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")
    
@router.get('/task', dependencies=[Depends(AuthValidator())], tags=['task'])
async def create_tasks( jwt_token: str = Depends(AuthValidator()),
                       mysql_session: AsyncSession = Depends(get_db),
):
    try:
        task_srv = task_service.TaskService(mysql_session)
        
        user = __user_model(jwt_token)
        user_id = user.get('user_id')
        
        query_result = await task_srv.get_tasks(user_id)
        
        return query_result
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")
    
@router.put('/task', dependencies=[Depends(AuthValidator())], tags=['task'])
async def create_tasks( request: UpdateTaskDto,
                       jwt_token: str = Depends(AuthValidator()),
                       mysql_session: AsyncSession = Depends(get_db),
):
    try:
        task_srv = task_service.TaskService(mysql_session)
        
        user = __user_model(jwt_token)
        user_id = user.get('user_id')
        
        query_result = await task_srv.update_task(request)
        
        if query_result._soft_closed != True:
            raise HTTPException
        
        return {
            "message": "Task updated successfully"
        }
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")
    
@router.delete('/task', dependencies=[Depends(AuthValidator())], tags=['task'])
async def create_tasks( request: TaskIdDto,
                       mysql_session: AsyncSession = Depends(get_db),
):
    try:
        task_srv = task_service.TaskService(mysql_session)
        
        query_result = await task_srv.delete_tasks(request.task_id)
        
        if query_result._soft_closed != True:
            raise HTTPException
        
        return {
            "message": "Task deleted successfully"
        }
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")
    
@router.put('/status', dependencies=[Depends(AuthValidator())], tags=['task'])
async def create_tasks( request: TaskIdDto,
                       mysql_session: AsyncSession = Depends(get_db),
):
    try:
        task_srv = task_service.TaskService(mysql_session)
        
        query_result = await task_srv.change_task_status(request.task_id)
        
        if query_result._soft_closed != True:
            raise HTTPException
        
        return {
            "message": "Task status changed successfully"
        }
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")
    
