from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

BaseTable = declarative_base()


class User(BaseTable):
    __tablename__ = "users"
    uid = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    canvasAccessToken = Column(String)
    googleCalendarAccessToken = Column(String)

class Course(BaseTable):
    __tablename__="courses"
    courseID=Column(Integer, primary_key=True, index=True)
    courseName= Column(String)
    profFName=Column(String)
    profLName=Column(String)
    crn=Column(Integer)
    uid = Column(Integer) #, ForeignKey('users.uid'))
    #user = relationship('User', back_populates='courses')

class Assignment(BaseTable):
    __tablename__="assignments"
    assignmentID = Column (Integer, primary_key=True, index=True)
    title= Column(String)
    description= Column(String)
    dueDate = Column(DateTime)
    courseID=Column(Integer) #, ForeignKey('courses.courseID'))
    #course= relationship('Course', back_populate='assignments')

