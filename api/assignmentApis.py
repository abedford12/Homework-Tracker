from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


from main.globalVars import USERNAME, PASSWORD, HOST, NAME
from models.tables import BaseTable, Course, Assignment
from models.userModels import courseResponse, courseCreate, assignmentResponse, assignmentCreate

conn_string = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}/{NAME}"
engine = create_engine(conn_string)
BaseTable.metadata.create_all(bind=engine)

engine = create_engine(conn_string)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API that gets a list of all the assignment in the database
@router.get("/{assignments_list}", response_model=list[assignmentResponse])
async def listAllAssignments(session: Session = Depends(get_db)):
    listOfAssignments = session.query(Assignment).all()
    return listOfAssignments


# API that gets a assignment based off their assignment id
@router.get("/{assignment_id}", response_model=assignmentResponse)
async def getAssignment(assignment_id: int, session: Session = Depends(get_db)):
    assignment = session.query(Assignment).filter(Assignment.assignmentID == assignment_id).first()
    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


# API that creates a new assignment for the database
@router.post("/{create_assignment}", response_model=assignmentCreate)
async def createAssignment(assignment: assignmentCreate, session: Session = Depends(get_db)):
    newAssignment = Assignment(**assignment.dict())
    session.add(newAssignment)
    session.commit()
    session.refresh(newAssignment)
    return newAssignment


# API that deletes a assignment based on assignment id in the database
@router.delete("/{assignment_id}", response_model=str)
async def deleteCourse(assignment_id: int, session: Session = Depends(get_db)):
    # Retrieve the Trip object by its ID
    assignmentDelete = session.query(Assignment).filter(Assignment.assignmentID == assignment_id).first()
    if assignmentDelete:
        # Delete the Trip object
        session.delete(assignmentDelete)
        session.commit()
        return f"Assignment {assignment_id} has now been deleted."
    else:
        raise HTTPException(status_code=404, detail="Assignment not found")