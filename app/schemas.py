from pydantic import BaseModel

class Team(BaseModel):
    id: int
    developers: int

class Project(BaseModel):
    id: int
    devs_nedeed: int