from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String

Base=declarative_base()

class Project(Base):
    __tablename__='projects'
    id=Column(Integer(),primary_key=True)
    name=Column(String(),unique=True,nullable=False)
    figma_file_path=Column(String(),nullable=True)
    github_link=Column(String(),nullable=True)

