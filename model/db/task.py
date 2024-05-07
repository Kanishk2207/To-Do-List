from typing import Literal

from model.db.RCBase import RCDBBase

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Enum

priority_enum = Literal['High','Mid','Low']
status_enum = Literal['completed','pending']

class Task(RCDBBase):
    __tablename__ = "task"
    task_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.user_id"))
    title: Mapped[str] = mapped_column(String(100))
    due_date: Mapped[int] = mapped_column()
    priority: Mapped[priority_enum] = mapped_column(Enum('High','Mid','Low'))
    status: Mapped[status_enum] = mapped_column(Enum('completed','pending'))
    created_at: Mapped[int] = mapped_column()
    updated_at: Mapped[int] = mapped_column()
    
    
    
    
    
    
    
    
# Table: task

# Columns:
# 	task_id	varchar(50) PK
# 	user_id	varchar(50)
# 	title	varchar(100)
# 	due_date	int
# 	priority	enum('High','Mid','Low')
# 	status	enum('completed','pending')
# 	created_at	int
# 	updated_at	int