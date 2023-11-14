from fastapi import FastAPI

from api import userApis, courseApis, assignmentApis

app=FastAPI()

app.include_router(userApis.router, prefix="/users", tags=["Users"])
app.include_router(courseApis.router, prefix="/courses", tags=["Courses"])
app.include_router(assignmentApis.router, prefix="/assignments", tags=["Assignments"])