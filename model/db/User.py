from model.db.TLBase import TLDBBase

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class User(TLDBBase):
    __tablename__ = "user"
    user_id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(45))
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[int] = mapped_column()
    updated_at: Mapped[int] = mapped_column()


