from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from broadcaster import Broadcast
from fastapi import FastAPI, Request

from app.graphql import type_defs
from models import engine, Base, db
from services.auth import auth_service

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ha-to-Pe File System",
    description="Ha-to-Pe File System",
    version="1.0.0",
)

bindables = []
schema = make_executable_schema(type_defs, *bindables)
broadcast = Broadcast("memory://")

def get_context_value(request: Request, *args):
    context = {
        "db": db,
        "pubsub": broadcast,
        "base_url": request.base_url
    }

    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        current_user = auth_service.get_user_from_token(token)
        if current_user:
            context["current_user"] = current_user
    return context


graphql_app = GraphQL(
    schema=schema,
    debug=True,
    context_value=get_context_value,
    # websocket_handler=GraphQLTransportWSHandler,
)

app.mount("/graphql", graphql_app)

@app.get("/")
def home():
    return {"message": "Ha-to-Pe is running..."}