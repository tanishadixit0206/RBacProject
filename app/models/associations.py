from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,ForeignKey,Integer,Table
Base =declarative_base()

user_group_role_assossiation_table=Table(
    Base.metadata,
    Column('group_id',Integer(),ForeignKey('group_roles.id'),primary_key=True),
    Column('user_id',Integer(),ForeignKey('users.id'),primary_key=True),
)

user_project_role_assossiation_table=Table(
    Base.metadata,
    Column('project_id',Integer(),ForeignKey('project_roles.id'),primary_key=True),
    Column('user_id',Integer(),ForeignKey('users.id'),primary_key=True),
)

# project_project_role_assossiation_table=Table(
#     Base.metadata,
#     Column('project_role_id',Integer(),ForeignKey('project_roles.id'),primary_key=True),
#     Column('project_id',Integer(),ForeignKey('projects.id'),primary_key=True),
# )