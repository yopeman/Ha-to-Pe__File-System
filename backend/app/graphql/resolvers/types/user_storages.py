from ariadne import ObjectType

user_storage_type = ObjectType("UserStorage")

@user_storage_type.field("id")
def resolve_user_storage_id(user_storage_obj, info):
    return user_storage_obj.id

@user_storage_type.field("user_id")
def resolve_user_id(user_storage_obj, info):
    return user_storage_obj.user_id

@user_storage_type.field("used_bytes")
def resolve_used_bytes(user_storage_obj, info):
    return user_storage_obj.used_bytes

@user_storage_type.field("quota_bytes")
def resolve_quota_bytes(user_storage_obj, info):
    return user_storage_obj.quota_bytes

@user_storage_type.field("created_at")
def resolve_created_at(user_storage_obj, info):
    return user_storage_obj.created_at

@user_storage_type.field("updated_at")
def resolve_updated_at(user_storage_obj, info):
    return user_storage_obj.updated_at