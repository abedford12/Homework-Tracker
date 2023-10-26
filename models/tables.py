from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

BaseTable=declarative_base()

class User(BaseTable):
    __tablename__="users"
    uid=Column(Integer, primary_key=True, index=True)
    email=Column(String)
    fname=Column(String)
    lname=Column(String)

