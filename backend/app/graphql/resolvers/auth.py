from ariadne import QueryType, MutationType

from services.auth import auth_service

query = QueryType()
mutation = MutationType()

@query.field("me")
def resolve_me(_, info):
    if 'current_user' not in info.context:
        raise Exception("User Not Found")
    return info.context['current_user']

@mutation.field("signup")
def resolve_signup(_, info, input):
    return auth_service.signup(
        username=input['username'],
        email=input['email'],
        password=input['password'],
    )

@mutation.field("login")
def resolve_login(_, info, input):
    return auth_service.login(
        email=input['email'],
        password=input['password']
    )

@mutation.field("update_my_profile")
def resolve_update_my_profile(_, info, input):
    if 'current_user' not in info.context:
        raise Exception("User Not Found")

    return auth_service.update_profile(
        user_id=info.context['current_user'].id,
        username=input['username'] if 'username' in input else None,
        email=input['email'] if 'email' in input else None,
        password=input['password'] if 'password' in input else None,
        role=input['role'] if 'role' in input else None,
    )

@mutation.field("delete_my_account")
def resolve_delete_my_account(_, info):
    if 'current_user' not in info.context:
        raise Exception("User Not Found")

    return auth_service.delete_profile(
        user_id=info.context['current_user'].id,
    )