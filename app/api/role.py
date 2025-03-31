from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User
from app.models.secrets import SecretsFile
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.utils import decode_jwt,is_project_manager_or_admin,is_admin
from app.security.encrypt_decrypt import SecurityManager
router = APIRouter()
security_manager=SecurityManager()

def assignGroupRole():
    return

def assignProjectRole():
    return
