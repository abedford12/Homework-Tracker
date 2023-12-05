from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from main.globalVars import USERNAME, PASSWORD, HOST, NAME
from models.tables import BaseTable, Course
from models.userModels import courseResponse, courseCreate

from typing import List

conn_string = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}/{NAME}"
engine = create_engine(conn_string)
BaseTable.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API that gets a list of all the courses in the database
@router.get("/{course_list}", response_model=list[courseResponse])
async def listAllCourses(session: Session = Depends(get_db)):
    listOfCourses = session.query(Course).all()
    return listOfCourses


# API that gets an array of crns based off their course id
@router.get("/crn_list/{course_id}", response_model=List[str])
async def getCourse(user_id: int, session: Session = Depends(get_db)):
    courses = session.query(Course).filter(Course.uid == user_id).all()
    if courses is None:
        raise HTTPException(status_code=404, detail="Course not found")
    crns = [course.crn for course in courses]
    return crns


# API that gets a course based on the id given
@router.get("/{course_id}", response_model=courseResponse)
async def getCourse(course_id: int, session: Session = Depends(get_db)):
    course = session.query(Course).filter(Course.courseID == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# API that creates a new course for the database
@router.post("/create/{create_course}", response_model=courseCreate)
async def createCourse(course: courseCreate, session: Session = Depends(get_db)):
    newCourse = Course(**course.dict())
    session.add(newCourse)
    session.commit()
    session.refresh(newCourse)
    return newCourse


# API that deletes a course based on courseid in the database
@router.delete("/{course_id}", response_model=str)
async def deleteCourse(course_id: int, session: Session = Depends(get_db)):
    courseDelete = session.query(Course).filter(Course.courseID == course_id).first()
    if courseDelete:
        session.delete(courseDelete)
        session.commit()
        return f"Course with the following ID has been deleted: {course_id} "
    else:
        raise HTTPException(status_code=404, detail="Course not found")
