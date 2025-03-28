from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String,LargeBinary

Base=declarative_base()

class SecretsFile(Base):
    id=Column(Integer(),primary_key=True)
    name=Column(String(),nullable=False)
    content=Column(LargeBinary,nullable=False)

class SecretKey(Base):
    id=Column(Integer(),primary_key=True)
    key=Column(String(),nullable=False)
