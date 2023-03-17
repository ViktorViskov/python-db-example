from dataclasses import dataclass


# model for user object
@dataclass
class User:
    id:int
    name:str
    surname:str
    email:str