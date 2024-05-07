from os import environ as env

from fastapi import FastAPI

from routers import auth

app = FastAPI()

app.include_router(auth.router)


@app.get('/', tags=['base'])
async def root():
    return {
        "message": "welcome to the app"
    }