from fastapi import FastAPI

from api import userApis

app=FastAPI()

app.include_router(userApis.router, prefix="/users", tags=["Users"])
