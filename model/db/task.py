from typing import Literal

from model.db.RCBase import RCDBBase

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Enum

priority_enum = Literal['high','mid','low']
status_enum = Literal['completed','pending']

class Task(RCDBBase):
    __tablename__ = "task"
    task_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.user_id"))
    title: Mapped[str] = mapped_column(String(100))
    due_date: Mapped[int] = mapped_column()
    priority: Mapped[priority_enum] = mapped_column(Enum('high','mid','low'))
    status: Mapped[status_enum] = mapped_column(Enum('completed','pending'))
    created_at: Mapped[int] = mapped_column()
    updated_at: Mapped[int] = mapped_column()
    