from app.models.role import GroupRoleEnum
from app.models.user import User

def is_admin(user:User):
    return any(role.name == GroupRoleEnum.ADMIN for role in user.group_roles)