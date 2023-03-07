# schema.py
import os
from ariadne import QueryType, MutationType, make_executable_schema,\
      load_schema_from_path, gql, ScalarType
from users.query_resolvers import (
    resolve_getAllUsers,
    resolve_getUserById,
    resolve_getProfileById,
    resolve_getAllProfiles,
    resolve_getAllUserLogs,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema_path = os.path.join(BASE_DIR, 'schema.graphql')

type_defs = gql(load_schema_from_path(schema_path))

query = QueryType()
mutation = MutationType()

# resolvers

query.set_field('getAllUsers', resolve_getAllUsers)
query.set_field('getUserById', resolve_getUserById)
query.set_field('getProfileById', resolve_getProfileById)
query.set_field('getAllProfiles', resolve_getAllProfiles)
query.set_field('getAllUserLogs', resolve_getAllUserLogs)   

schema = make_executable_schema(
    type_defs,
    query, 
    mutation
)