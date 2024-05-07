from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from helpers import user_token_helper
from internal.database.mysql import get_db
from model.dto.auth_dto import User as UserDto
from utils.token_generator import __user_model
from services import auth_service

router = APIRouter()

@router.post('/register', tags = ['auth'])
async def create_user(request: UserDto, mysql_session: AsyncSession = Depends(get_db)):
    try:
        auth_srv = auth_service.AuthService(mysql_session)
        
        user = await auth_srv.create_user(request.email, request.password)
        
        return {
            'message': "Registered successfully, please login"
        }
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")

@router.get('/login', tags=['auth'])
async def get_user(request: UserDto, mysql_session: AsyncSession = Depends(get_db)):
    try:
        auth_srv = auth_service.AuthService(mysql_session)
        
        user = await auth_srv.get_user(request.email, request.password)
        
        token = user_token_helper.generate_user_token(user)
        
        return {
            "user_id": user.user_id,
            "token": token
        }
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")