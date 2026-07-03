from ariadne import ObjectType

user_type = ObjectType("User")

@user_type.field("id")
def resolve_user_id(user_obj, info):
    return user_obj.id

@user_type.field("username")
def resolve_user_id(user_obj, info):
    return user_obj.username

@user_type.field("email")
def resolve_user_id(user_obj, info):
    return user_obj.email

@user_type.field("role")
def resolve_user_id(user_obj, info):
    return user_obj.role.name

@user_type.field("created_at")
def resolve_user_id(user_obj, info):
    return user_obj.created_at

@user_type.field("updated_at")
def resolve_user_id(user_obj, info):
    return user_obj.updated_at

@user_type.field("deleted_at")
def resolve_user_id(user_obj, info):
    return user_obj.deleted_at