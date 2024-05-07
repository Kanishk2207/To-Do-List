from os import environ as env

from fastapi import FastAPI


app = FastAPI()


@app.get('/', tags=['base'])
async def root():
    return {
        "message": "welcome to the app"
    }