# schema.py
import os
from ariadne import QueryType, MutationType, make_executable_schema, load_schema_from_path, gql

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema_path = os.path.join(BASE_DIR, 'schema.graphql')

type_defs = gql(load_schema_from_path(schema_path))

query = QueryType()
mutation = MutationType()

# resolvers

schema = make_executable_schema(type_defs, query, mutation)