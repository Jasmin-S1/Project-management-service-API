from sqlalchemy import ARRAY, Boolean, Column, Integer
from .database import Base


class Teams(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, nullable=False)
    developers = Column(Integer, nullable=False)
    idle_developers = Column(Integer, nullable=False)
    assigned_projects = Column(ARRAY(Integer))



class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, nullable=False)
    devs_nedeed = Column(Integer, nullable=False)
    