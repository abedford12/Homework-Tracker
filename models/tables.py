from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

BaseTable=declarative_base()

class User(BaseTable):
    __tablename__="users"
    uid=Column(Integer, primary_key=True, index=True)
    email=Column(String)
    fname=Column(String)
    lname=Column(String)

class Course(BaseTable):
    __tablename__="courses"
    courseName=Column(String)
    courseCode=Column(String)
    courseID=Column(String, primary_key=True)
    courseNickName=Column(String)

