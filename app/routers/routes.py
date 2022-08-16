from fastapi import status, HTTPException, APIRouter
import psycopg2
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

HOSTNAME = os.getenv('DATABASE_HOSTNAME')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

router = APIRouter()

class Teams(BaseModel):
    id: int
    developers: int

class Projects(BaseModel):
    id: int
    devs_nedeed: int

conn = psycopg2.connect(
            host=HOSTNAME,
            database=DATABASE_NAME,
            user=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
)

cursor = conn.cursor()

def delete_all():
    cursor.execute("DELETE FROM teams")
    cursor.execute("DELETE FROM projects")
    conn.commit()   


@router.get("/status")
def get_status():
    if(conn):
        return {"message": "Connection successfull"}
    return {"message": "Connection false"}
   

@router.put("/teams")
def available_teams(teams: List[Teams]):
    delete_all()
    for i in range(len(teams)):
        cursor.execute("""INSERT INTO teams (id, developers, idle_developers) VALUES (%s, %s, %s)""", (teams[i].id, teams[i].developers, teams[i].developers))
        conn.commit()
    return teams


@router.post("/project")
def post_new_project(project: Projects):
    cursor.execute("""INSERT INTO projects VALUES (%s, %s)""", (project.id, project.devs_nedeed))
    cursor.execute("""SELECT id FROM teams WHERE idle_developers >= %s""", ([project.devs_nedeed]))
    choosed_team = cursor.fetchone()
    cursor.execute("""UPDATE teams SET assigned_projects = ARRAY_APPEND(assigned_projects, %s) , idle_developers = idle_developers - %s WHERE id = %s""", (project.id, project.devs_nedeed ,choosed_team))
    conn.commit()


@router.post("/completed/{id}")
def project_completed(id: int):
    cursor.execute("""SELECT id FROM projects WHERE id=%s""", (str(id)))
    result = cursor.fetchone()
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Project with id:{id} not found')
    raise HTTPException(status_code=status.HTTP_200_OK)


@router.post("/assigned/{id}")
def project_assigned(id: int):
    cursor.execute("""SELECT id, assigned_projects FROM teams WHERE %s = ANY(assigned_projects)""", (str(id)))
    result= cursor.fetchone()
    if result == None:
        cursor.execute("""SELECT id FROM projects WHERE id=%s""", (str(id)))
        result = cursor.fetchone()
        if result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_200_OK, detail=f'Project with id: {id} is assigned to team with id: {result[0]}')
   
    
   
