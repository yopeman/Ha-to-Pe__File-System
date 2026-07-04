from ariadne import ObjectType

share_type = ObjectType("ShareType")

@share_type.field("id")
def resolve_share_id(share_obj, info):
    return share_obj.id

@share_type.field("user_id")
def resolve_user_id(share_obj, info):
    return share_obj.user_id

@share_type.field("node_id")
def resolve_node_id(share_obj, info):
    return share_obj.node_id

@share_type.field("group_id")
def resolve_group_id(share_obj, info):
    return share_obj.group_id

@share_type.field("status")
def resolve_status(share_obj, info):
    return share_obj.status.name

@share_type.field("created_at")
def resolve_created_at(share_obj, info):
    return share_obj.created_at

@share_type.field("updated_at")
def resolve_updated_at(share_obj, info):
    return share_obj.updated_at

@share_type.field("expired_at")
def resolve_expired_at(share_obj, info):
    return share_obj.expired_at

@share_type.field("accepted_at")
def resolve_accepted_at(share_obj, info):
    return share_obj.accepted_at

@share_type.field("deleted_at")
def resolve_deleted_at(share_obj, info):
    return share_obj.deleted_at