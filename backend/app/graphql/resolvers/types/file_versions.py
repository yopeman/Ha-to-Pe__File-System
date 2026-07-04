from ariadne import ObjectType

file_version_type = ObjectType("FileVersion")

@file_version_type.field("id")
def resolve_file_version_id(file_version_obj, info):
    return file_version_obj.id

@file_version_type.field("node_id")
def resolve_node_id(file_version_obj, info):
    return file_version_obj.node_id

@file_version_type.field("version_number")
def resolve_version_number(file_version_obj, info):
    return file_version_obj.version_number

@file_version_type.field("storage_path")
def resolve_storage_path(file_version_obj, info):
    return file_version_obj.storage_path

@file_version_type.field("size")
def resolve_size(file_version_obj, info):
    return file_version_obj.size

@file_version_type.field("creator_id")
def resolve_creator_id(file_version_obj, info):
    return file_version_obj.creator_id

@file_version_type.field("created_at")
def resolve_created_at(file_version_obj, info):
    return file_version_obj.created_at

@file_version_type.field("deleted_at")
def resolve_deleted_at(file_version_obj, info):
    return file_version_obj.deleted_at