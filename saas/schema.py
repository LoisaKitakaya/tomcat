# schema.py
import os
import time

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
    resolve_getUserByUsername,
    resolve_getUserByPublicId,
    resolve_getProfileByPublicId,
    resolve_getAllProfiles,
    resolve_getAllUserLogs,
    resolve_getUserLogsByUserPublicId,
    resolve_getAllWorkspaces,
    resolve_getWorkspaceByPublicId
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema_path = os.path.join(BASE_DIR, 'schema.graphql')

type_defs = gql(load_schema_from_path(schema_path))

# scaler types

datetime_scalar = ScalarType("Datetime")

@datetime_scalar.serializer
def serialize_datetime(value):

    date = time.mktime(value.timetuple())

    return str(date)

# query and mutation types

query = QueryType()
mutation = MutationType()

# resolvers

query.set_field('getAllUsers', resolve_getAllUsers)
query.set_field('getUserByPublicId', resolve_getUserByPublicId)
query.set_field('getUserByUsername', resolve_getUserByUsername)

query.set_field('getAllProfiles', resolve_getAllProfiles)
query.set_field('getProfileByPublicId', resolve_getProfileByPublicId)

query.set_field('getAllUserLogs', resolve_getAllUserLogs)
query.set_field('getUserLogsByUserPublicId', resolve_getUserLogsByUserPublicId)

query.set_field('getAllWorkspaces', resolve_getAllWorkspaces)
query.set_field('getWorkspaceByPublicId', resolve_getWorkspaceByPublicId)   

schema = make_executable_schema(
    type_defs,
    query, 
    mutation,
    datetime_scalar
)