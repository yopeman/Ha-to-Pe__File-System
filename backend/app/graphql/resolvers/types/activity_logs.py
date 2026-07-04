from ariadne import ObjectType

activity_log_type = ObjectType("ActivityLog")

@activity_log_type.field("id")
def resolve_activity_log_id(activity_log_obj, info):
    return activity_log_obj.id

@activity_log_type.field("user_id")
def resolve_user_id(activity_log_obj, info):
    return activity_log_obj.user_id

@activity_log_type.field("node_id")
def resolve_node_id(activity_log_obj, info):
    return activity_log_obj.node_id

@activity_log_type.field("action")
def resolve_action(activity_log_obj, info):
    return activity_log_obj.action

@activity_log_type.field("metadata")
def resolve_metadata(activity_log_obj, info):
    return activity_log_obj.metadata

@activity_log_type.field("created_at")
def resolve_created_at(activity_log_obj, info):
    return activity_log_obj.created_at