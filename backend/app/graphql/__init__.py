from pathlib import Path
from ariadne import load_schema_from_path

schema_dir = Path(__file__).parent
schema_files = schema_dir.glob("*.gql")

type_defs = [load_schema_from_path(file) for file in schema_files]

with open("./app/graphql/schema.graphql", "w") as file:
    file.write("\n\n".join(type_defs))