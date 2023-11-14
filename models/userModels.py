from pydantic import BaseModel
from datetime import datetime


class userResponse(BaseModel):
    uid: int
    username: str
    canvasAccessToken: str
    googleCalendarAccessToken: str


class userCreate(BaseModel):
    username: str
    canvasAccessToken: str
    googleCalendarAccessToken: str


class courseResponse(BaseModel):
    courseID: int
    courseName: str
    crn: int
    profFName: str
    profLName: str
    uid: int


class courseCreate(BaseModel):
    courseName: str
    crn: int
    profFName: str
    profLName: str
    uid: int


class assignmentResponse(BaseModel):
    assignmentID: int
    title: str
    description: str
    dueDate: datetime
    courseID: int


class assignmentCreate(BaseModel):
    title: str
    description: str
    dueDate: datetime
    courseID: int
