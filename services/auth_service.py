import time 

from asyncmy.errors import DatabaseError
from fastapi import HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from model.dto.auth_dto import User as UserDto
from model.db.User import User
from services.rc_db_Service import RCDBService
from utils import uuid_generator, password_hasher, token_generator

class AuthService(RCDBService):
    
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.session = session
    
    async def create_user(self, email, password):
        try:
            
            user_id = uuid_generator.get_uuid()
            now = time.time()
            hashed_password = password_hasher.hash_password(password)
            
            user = User(
                user_id = user_id,
                email = email,
                password = hashed_password,
                created_at = int(now),
                updated_at = int(now)
            )
            
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            
            return user
        
        except IntegrityError as integrity_error:
            if "Duplicate entry" in str(integrity_error.orig):
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email already exists, please login.")
            else:
                raise HTTPException(status_code=500, detail=f"Integrity Error: {str(integrity_error)}")
        except DatabaseError as db_error:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(db_error)}")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")
    
    async def get_user(self, email, password):
        try:
            password_hash = password_hasher.hash_password(password)
            
            query = (
                select(User)
                .where(
                    and_(
                        User.email == email,
                    )
                )
            )
            
            user = (await self.session.execute(query)).scalars().one_or_none()
            
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: Email cannot be found, create account")
            if user.password != password_hash:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error: Password incorrect, try again")
                
            
            return user
        except DatabaseError as db_error:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(db_error)}")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(ex)}")