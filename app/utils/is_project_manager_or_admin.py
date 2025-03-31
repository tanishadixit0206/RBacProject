from app.models.role import ProjectRoleEnum
from app.models.user import User

def is_project_manager_or_admin(user:User,projectid:int):
    return any(((role.name == ProjectRoleEnum.ADMIN or role.name==ProjectRoleEnum.PROJECT_MANAGER) and(role.projectid==projectid)) for role in user.project_roles)