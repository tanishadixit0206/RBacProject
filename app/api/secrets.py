from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User
from app.models.secrets import SecretsFile
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.utils import decode_jwt,is_project_manager_or_admin,is_admin
from app.security.encrypt_decrypt import SecurityManager
router = APIRouter()
security_manager=SecurityManager()
@router.put("/create")
async def createSecret(token:str,secret:SecretsFile,db:Session=Depends(get_db)):
    try:
        if not token:
            raise HTTPException(status_code=401,detail="Token not found")
        
        current_userid=decode_jwt(token)
        current_user=db.get(User,current_userid)
        if(not is_project_manager_or_admin(current_user)):
            raise HTTPException(status_code=403,detail="Only group admin or project manager is allowed to create secrets file")
        
        found_secret=db.query(SecretsFile).filter(SecretsFile.name==secret.name).first()
        if found_secret:
            raise HTTPException(status_code=400,detail="Secrets file with given name already exists")
        
        db.add(secret)
        db.commit()
        db.refresh(secret)
        return {"message":"Secret created successfully"}
       
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))    
    
@router.get("/list/{secretid}")
async def getSecret(secretid:int,db:Session=Depends(get_db)):
    try:
        secret=db.get(SecretsFile,secretid)
        if not secret:
            raise HTTPException(status_code=404,detail="No secret found")
        return secret
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@router.put("/update/{secretid}")
async def updateSecret(secretid:int,token:str,secret_details:SecretsFile,db:Session=Depends(get_db)):
    try:
        if not token:
            raise HTTPException(status_code=401,detail="Token not found")
        
        current_userid=decode_jwt(token)
        current_user=db.get(User,current_userid)
        if(not is_project_manager_or_admin(current_user)):
            raise HTTPException(status_code=403,detail="Only group admin or project manager is allowed to update secrets file")
        
        secret=db.get(SecretsFile,secretid)
        if not secret:
            raise HTTPException(status_code=400,detail="Secret not found")
        
        for key,value in secret_details.dict().items():
            setattr(secret,key,value)
        db.commit()
        return {"message":"Secret updated successfully"}
       
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))
    
@router.put("/delete/{secretid}")
async def deleteSecret(secretid:int,token:str,db:Session=Depends(get_db)):
    try:
        if not token:
            raise HTTPException(status_code=401,detail="Token not found")
        
        current_userid=decode_jwt(token)
        current_user=db.get(User,current_userid)
        if(not is_project_manager_or_admin(current_user)):
            raise HTTPException(status_code=403,detail="Only group admin or project manager is allowed to delete secrets file")
        
        secret=db.get(SecretsFile,secretid)
        if not secret:
            raise HTTPException(status_code=400,detail="Secret not found")
        
        db.delete(secret)
        db.commit()
        return {"message":"Secret deleted"}
       
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))
    
