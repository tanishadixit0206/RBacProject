from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User
from app.models.projects import Project
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.utils import decode_jwt,is_admin
router = APIRouter()

@router.put("/create")
async def createProject(token:str,project:Project,db:Session=Depends(get_db)):
    try:
        if not token:
            raise HTTPException(status_code=401,detail="Token not found")
        
        current_userid=decode_jwt(token)
        current_user=db.get(User,current_userid)
        if(not is_admin(current_user)):
            raise HTTPException(status_code=403,detail="Only group admin is allowed to create projects")
        
        found_project=db.query(Project).filter(Project.name==project.name).first()
        if found_project:
            raise HTTPException(status_code=400,detail="Project already exists")
        
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
       
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))
    
@router.get("/list")
async def getProjectList(db:Session=Depends(get_db)):
    try:
        projects=db.get(Project)
        return projects
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/list/{projectid}")
async def getProject(projectid:int,db:Session=Depends(get_db)):
    try:
        project=db.get(Project,projectid)
        if not project:
            raise HTTPException(status_code=404,detail="No project found")
        return project
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@router.put("/update/{projectid}")
async def updateProject(projectid:int,token:str,project_details:Project,db:Session=Depends(get_db)):
    try:
        if not token:
            raise HTTPException(status_code=401,detail="Token not found")
        
        current_userid=decode_jwt(token)
        current_user=db.get(User,current_userid)
        if(not is_admin(current_user)):
            raise HTTPException(status_code=403,detail="Only group admin is allowed to update project details")
        
        project=db.get(Project,projectid)
        if not project:
            raise HTTPException(status_code=400,detail="Project not found")
        
        for key,value in project_details.dict().items():
            setattr(project,key,value)
        db.commit()
        return project
       
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))
    
@router.put("/delete/{projectid}")
async def deleteProject(projectid:int,token:str,db:Session=Depends(get_db)):
    try:
        if not token:
            raise HTTPException(status_code=401,detail="Token not found")
        
        current_userid=decode_jwt(token)
        current_user=db.get(User,current_userid)
        if(not is_admin(current_user)):
            raise HTTPException(status_code=403,detail="Only group admin is allowed to delete projects")
        
        project=db.get(Project,projectid)
        if not project:
            raise HTTPException(status_code=400,detail="Project not found")
        
        db.delete(project)
        db.commit()
        return {"message":"Project deleted"}
       
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))
    
