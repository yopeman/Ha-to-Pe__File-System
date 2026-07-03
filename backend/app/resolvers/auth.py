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