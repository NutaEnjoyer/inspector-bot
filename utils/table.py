from typing import List
from enum import Enum
from pydantic import BaseModel



class UserStatus(Enum):

    DEFAULT = 1
    ADMIN = 2


class User(BaseModel):

    index : int
    registered : float
    status : int
    claim : int
    mute : bool


class Word(BaseModel):

    index : str
    word : List[str]
    message : str


class GroupMessage(BaseModel):

    index : int
    chat_id : int
    sender : int
    time : float
    

class City(BaseModel):

    index : str
    message : str
    word : List[str]
    channel_url : int

