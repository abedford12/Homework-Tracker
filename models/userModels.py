from pydantic import BaseModel


class userResponse(BaseModel):
    uid:int
    email:str
    fname:str
    lname:str

class userCreate(BaseModel):
    email: str
    fname: str
    lname: str