from ariadne import QueryType

query = QueryType()

@query.field("me")
def resolve_me(_, info):
    return info.context.user