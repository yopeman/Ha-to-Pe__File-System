from ariadne import ObjectType

node_type = ObjectType("Node")

@node_type.field("id")
def resolve_node_id(node_obj, info):
    return node_obj.id

@node_type.field("parent_id")
def resolve_parent_id(node_obj, info):
    return node_obj.parent_id

@node_type.field("owner_id")
def resolve_owner_id(node_obj, info):
    return node_obj.owner_id

@node_type.field("name")
def resolve_name(node_obj, info):
    return node_obj.name

@node_type.field("type")
def resolve_type(node_obj, info):
    return node_obj.type.name

@node_type.field("visibility")
def resolve_visibility(node_obj, info):
    return node_obj.visibility

@node_type.field("created_at")
def resolve_created_at(node_obj, info):
    return node_obj.created_at

@node_type.field("updated_at")
def resolve_updated_at(node_obj, info):
    return node_obj.updated_at

@node_type.field("hidden_at")
def resolve_hidden_at(node_obj, info):
    return node_obj.hidden_at

@node_type.field("trashed_at")
def resolve_trashed_at(node_obj, info):
    return node_obj.trashed_at

@node_type.field("deleted_at")
def resolve_deleted_at(node_obj, info):
    return node_obj.deleted_at