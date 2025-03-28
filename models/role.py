from sqlalchemy import Column,String,Integer, Enum
from sqlalchemy.orm import declarative_base,relationship
import enum
from associations import user_group_role_assossiation_table,user_project_role_assossiation_table
Base=declarative_base()

class ProjectRoleEnum(enum.Enum):
    ADMIN='admin'
    PROJECT_MANAGER='project_manager'
    MEMBER='member'

class GroupRoleEnum(enum.Enum):
    B28='b28'
    B27='b27'
    B26='b26'
    B25='b25'

class RoleType(enum.Enum):
    GROUP='group'
    PROJECT='project'

class ProjectRole(Base):
    __tablename__='project_roles'
    id=Column(Integer(),primary_key=True)
    name=Column(
        Enum(ProjectRoleEnum),
        default=ProjectRoleEnum.MEMBER,
        nullable=False
    )
    project=Column(String(),nullable=False)
    users=relationship('User',secondary=user_project_role_assossiation_table,back_populates='project_roles')

class GroupRole(Base):
    id=Column(Integer(),primary_key=True)
    name=Column(
        Enum(GroupRoleEnum),
        default=GroupRoleEnum.B28,
        nullable=False
    )
    users=relationship('User',secondary=user_group_role_assossiation_table,back_populates='group_roles')

