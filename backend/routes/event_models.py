from pydantic import BaseModel
from typing import List


class ImageModel(BaseModel):
    data : List[str]


class UserModel(BaseModel):
    username : str
    password : str

class RegisterModel(BaseModel):
    name : str
    birthdate : int
    email : str
    username : str
    password : str

