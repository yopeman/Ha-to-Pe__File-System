from ariadne import QueryType, MutationType

from services.auth import auth_service

query = QueryType()
mutation = MutationType()

@query.field("me")
def resolve_me(_, info):
    if 'user' not in info.context:
        raise Exception("User Not Found")

    print(
        '\n\n\n',
        '='*72,
        '\n\n\n',
        info.context,
        '\n\n\n',
        '='*72,
        '\n\n\n',
    )

    return info.context['user']

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