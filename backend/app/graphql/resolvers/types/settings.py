from ariadne import ObjectType

setting_type = ObjectType("Setting")

@setting_type.field("free_storage_gb")
def resolve_free_storage_gb(setting_obj, info):
    return setting_obj.free_storage_gb

@setting_type.field("price_per_gb")
def resolve_price_per_gb(setting_obj, info):
    return setting_obj.price_per_gb

@setting_type.field("trash_retention_days")
def resolve_trash_retention_days(setting_obj, info):
    return setting_obj.trash_retention_days

@setting_type.field("created_at")
def resolve_created_at(setting_obj, info):
    return setting_obj.created_at