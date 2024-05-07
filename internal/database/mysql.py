from os import environ as env

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_uri():
    return "mysql+asyncmy://{}:{}@{}/{}".format(env['DB_USER'], env['DB_PASSWORD'], env['DB_URL'], env['DB_NAME'], )


engine = create_async_engine(get_uri(), echo=True)

SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception as ex:
            await db.rollback()
        finally:
            await db.close()
