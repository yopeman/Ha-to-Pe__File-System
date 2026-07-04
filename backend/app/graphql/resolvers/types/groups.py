from ariadne import ObjectType

group_type = ObjectType("GroupType")

@group_type.field("id")
def resolve_group_id(group_obj, info):
    return group_obj.id

@group_type.field("name")
def resolve_name(group_obj, info):
    return group_obj.name

@group_type.field("creator_id")
def resolve_creator_id(group_obj, info):
    return group_obj.creator_id

@group_type.field("created_at")
def resolve_created_at(group_obj, info):
    return group_obj.created_at

@group_type.field("updated_at")
def resolve_updated_at(group_obj, info):
    return group_obj.updated_at

@group_type.field("deleted_at")
def resolve_deleted_at(group_obj, info):
    return group_obj.deleted_at