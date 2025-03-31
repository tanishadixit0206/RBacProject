import jwt
import os

def decode_jwt(token:str):
    payload= jwt.decode(token,os.getenv("JWT_SECRET_KEY"),algorithms="HS256")
    return payload.get("userid")
