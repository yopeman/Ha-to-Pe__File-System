from ariadne import ObjectType

oauth_type = ObjectType("OAuthAccount")

@oauth_type.field("id")
def resolve_oauth_id(oauth_obj, info):
    return oauth_obj.id

@oauth_type.field("user_id")
def resolve_user_id(oauth_obj, info):
    return oauth_obj.user_id

@oauth_type.field("provider")
def resolve_provider(oauth_obj, info):
    return oauth_obj.provider

@oauth_type.field("provider_user_id")
def resolve_provider_user_id(oauth_obj, info):
    return oauth_obj.provider_user_id

@oauth_type.field("created_at")
def resolve_created_at(oauth_obj, info):
    return oauth_obj.created_at

@oauth_type.field("updated_at")
def resolve_updated_at(oauth_obj, info):
    return oauth_obj.updated_at