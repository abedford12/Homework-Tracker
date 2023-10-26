from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from main.globalVars import USERNAME, PASSWORD, HOST, NAME
from models.tables import BaseTable, User
from models.userModels import userResponse, userCreate

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

@router.get("", response_model=list[userResponse])
async def listAllUsers(session: Session=Depends(get_db)):
    listOfUsers=session.query(User).all()
    return listOfUsers

@router.post("", response_model=userResponse)
async def createUser(user: userCreate, session: Session = Depends(get_db)):
    newUser = User(**user.dict())
    session.add(newUser)
    session.commit()
    session.refresh(newUser)
    return newUser