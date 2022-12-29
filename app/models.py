from pydantic import BaseModel
from typing import (
    Optional,
    Union,
    List,
)

class Endpoint(BaseModel):
    owner_username: str
    url: str

class User(BaseModel):
    username: str
    password_hash: str
    endpoints: Optional[List[Endpoint]] = []

class UserOut(BaseModel):
    username: str
    endpoints: Optional[List[Endpoint]] = []
    
class UserReg(BaseModel):
    username: str
    password: str
