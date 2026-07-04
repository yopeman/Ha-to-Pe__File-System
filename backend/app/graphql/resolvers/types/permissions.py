from ariadne import ObjectType

permission_type = ObjectType("Permission")

@permission_type.field("id")
def resolve_permission_id(permission_obj, info):
    return permission_obj.id

@permission_type.field("group_id")
def resolve_group_id(permission_obj, info):
    return permission_obj.group_id

@permission_type.field("list")
def resolve_list(permission_obj, info):
    return permission_obj.list

@permission_type.field("read_metadata")
def resolve_read_metadata(permission_obj, info):
    return permission_obj.read_metadata

@permission_type.field("create_file")
def resolve_create_file(permission_obj, info):
    return permission_obj.create_file

@permission_type.field("create_directory")
def resolve_create_directory(permission_obj, info):
    return permission_obj.create_directory

@permission_type.field("rename")
def resolve_rename(permission_obj, info):
    return permission_obj.rename

@permission_type.field("move")
def resolve_move(permission_obj, info):
    return permission_obj.move

@permission_type.field("copy")
def resolve_copy(permission_obj, info):
    return permission_obj.copy

@permission_type.field("delete")
def resolve_delete(permission_obj, info):
    return permission_obj.delete

@permission_type.field("restore")
def resolve_restore(permission_obj, info):
    return permission_obj.restore

@permission_type.field("purge")
def resolve_purge(permission_obj, info):
    return permission_obj.purge

@permission_type.field("download")
def resolve_download(permission_obj, info):
    return permission_obj.download

@permission_type.field("zip")
def resolve_zip(permission_obj, info):
    return permission_obj.zip

@permission_type.field("share")
def resolve_share(permission_obj, info):
    return permission_obj.share

@permission_type.field("manage_visibility")
def resolve_manage_visibility(permission_obj, info):
    return permission_obj.manage_visibility

@permission_type.field("manage_permission")
def resolve_manage_permission(permission_obj, info):
    return permission_obj.manage_permission

@permission_type.field("manage_owner")
def resolve_manage_owner(permission_obj, info):
    return permission_obj.manage_owner

@permission_type.field("created_at")
def resolve_created_at(permission_obj, info):
    return permission_obj.created_at

@permission_type.field("updated_at")
def resolve_updated_at(permission_obj, info):
    return permission_obj.updated_at