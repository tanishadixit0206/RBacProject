from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import String, Column,Integer,Date
from associations import user_group_role_assossiation_table
from associations import user_project_role_assossiation_table

Base=declarative_base()

class User(Base):
    __tablename__='users'
    id=Column(Integer(),primary_key=True)
    username=Column(String(),nullable=False,unique=True)
    email=Column(String(),unique=True)
    password=Column(String(),nullable=False)
    enrollment_no=Column(Integer(),unique=True,nullable=False)
    github_id=Column(String(),unique=True,nullable=True)
    phone_no=Column(Integer(),nullable=True)
    birthday=Column(Date(),nullable=True)
    project_roles=relationship('ProjectRole',secondary=user_project_role_assossiation_table,back_populates='users')
    group_roles=relationship('GroupRole',secondary=user_group_role_assossiation_table,back_populates='users')