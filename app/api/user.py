from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.security.encrypt_decrypt import SecurityManager
from app.utils import create_jwt,decode_jwt,is_admin
router = APIRouter()
security_manager=SecurityManager()

@router.post("/register")
async def register(user: User,db:Session=Depends(get_db)):
    try:
        found_user=db.query(User).filter(User.email==user.email).first()
        if found_user:
            raise HTTPException(status_code=400,detail="User already exists")
        user.password=security_manager.hash_password(user.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message":"User registered successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))

@router.post("/login")
async def login(user: User,db:Session=Depends(get_db)):
    try:
        db_user=db.query(User).filter(User.email==user.email).first()
        if not db_user:
            raise HTTPException(status_code=400,detail="No user with the given credentials found")
        if not security_manager.verify_password(user.password,db_user.password):
            raise HTTPException(status_code=400,detail="Invalid credentials")
        access_token=create_jwt({"userid":db_user.id})
        return {"access_token":access_token}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@router.get("/list")
async def getUserList(db:Session=Depends(get_db)):
    try:
        users=db.get(User)
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/list/{userid}")
async def getUser(userid:int,db:Session=Depends(get_db)):
    try:
        user=db.get(User,userid)
        if not user:
            raise HTTPException(status_code=404,detail="No user found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@router.put("/update/{userid}")
async def updateUser(userid:int,token:str,user_details:User,db:Session=Depends(get_db)):
    try:
        if not token:
            raise HTTPException(status_code=401,detail="Token not found")
        
        current_userid=decode_jwt(token)
        current_user=db.get(User,current_userid)
        if(not is_admin(current_user)):
            raise HTTPException(status_code=403,detail="Only group admin is allowed to update user details")
        
        user=db.get(User,userid)
        if not user:
            raise HTTPException(status_code=400,detail="User not found")
        
        for key,value in user_details.dict().items():
            setattr(user,key,value)
        db.commit()
        return user 
       
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))
    
@router.put("/delete/{userid}")
async def deleteUser(userid:int,token:str,db:Session=Depends(get_db)):
    try:
        if not token:
            raise HTTPException(status_code=401,detail="Token not found")
        
        current_userid=decode_jwt(token)
        current_user=db.get(User,current_userid)
        if(not is_admin(current_user)):
            raise HTTPException(status_code=403,detail="Only group admin is allowed to delete users")
        
        user=db.get(User,userid)
        if not user:
            raise HTTPException(status_code=400,detail="User not found")
        
        db.delete(user)
        db.commit()
        return {"message":"User deleted"}
       
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))
    
