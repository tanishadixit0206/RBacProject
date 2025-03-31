from datetime import timedelta,datetime
import jwt
import os

def create_jwt(data:dict, expires_delta:timedelta|None=None):
    data=data.copy()
    expire_time=datetime.now()+timedelta(minutes=30)
    data.update({"exp":expire_time})
    return jwt.encode(data,os.getenv("JWT_SECRET_KEY"),"HS256")
