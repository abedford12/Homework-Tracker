from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from main.globalVars import USERNAME, PASSWORD, HOST, NAME
from models.tables import BaseTable, User
from models.userModels import userResponse, userCreate

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


# API that gets a list of all the users in the database
@router.get("/user_list", response_model=list[userResponse])
async def listAllUsers(session: Session = Depends(get_db)):
    listOfUsers = session.query(User).all()
    return listOfUsers


# API that gets a user based off their user id
@router.get("/id_retrieve/{user_id}", response_model=userResponse)
async def getUser(user_id: int, session: Session = Depends(get_db)):
    user = session.query(User).filter(User.uid == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# API that gets a user based off their Canvas Token
@router.get("/CAT_retrieve/{user_CAT}", response_model=dict)
async def getUser(user_CAT: str, session: Session = Depends(get_db)):
    user = session.query(User).filter(User.canvasAccessToken == user_CAT).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    uid= {"user_uid": user.uid}

    return uid


# API that creates a new user for the database
@router.post("/create/{create_user}", response_model=userResponse)
async def createUser(user: userCreate, session: Session = Depends(get_db)):
    newUser = User(**user.dict())
    session.add(newUser)
    session.commit()
    session.refresh(newUser)
    return newUser


# API that deletes a trip by its user id
@router.delete("/{user_id}", response_model=str)
async def deleteUser(user_id: int, session: Session = Depends(get_db)):
    userToDelete = session.query(User).filter(User.uid == user_id).first()
    if userToDelete:
        session.delete(userToDelete)
        session.commit()
        return f"User with the following ID has been deleted: {user_id} "
    else:
        raise HTTPException(status_code=404, detail="User not found")
