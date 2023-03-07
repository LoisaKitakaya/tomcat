# schema.py
import os
from ariadne import (
    QueryType,
    ScalarType,
    MutationType,
    make_executable_schema,
    load_schema_from_path,
    gql
)

from users.query_resolvers import (
    resolve_getAllUsers,
    resolve_getUserById,
    resolve_getProfileById,
    resolve_getAllProfiles,
    resolve_getAllUserLogs,
    resolve_getUserLogsByUserId,
    resolve_getWorkspaceById
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema_path = os.path.join(BASE_DIR, 'schema.graphql')

type_defs = gql(load_schema_from_path(schema_path))

# scaler types

datetime_scalar = ScalarType("Datetime")

@datetime_scalar.serializer
def serialize_datetime(value):

    return value.isoformat()

# query and mutation types

query = QueryType()
mutation = MutationType()

# resolvers

query.set_field('getAllUsers', resolve_getAllUsers)
query.set_field('getUserById', resolve_getUserById)

query.set_field('getProfileById', resolve_getProfileById)
query.set_field('getAllProfiles', resolve_getAllProfiles)

query.set_field('getAllUserLogs', resolve_getAllUserLogs)
query.set_field('getUserLogsByUserId', resolve_getUserLogsByUserId)

query.set_field('getWorkspaceById', resolve_getWorkspaceById)   

schema = make_executable_schema(
    type_defs,
    query, 
    mutation,
    datetime_scalar
)