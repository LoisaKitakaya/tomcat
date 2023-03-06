# schema.py
import os
from ariadne import QueryType, MutationType, make_executable_schema, load_schema_from_path, gql
from users.query_resolvers import (
    resolve_getAllUsers,
    resolve_getUserById,
    resolve_getProfileByPublicId,
    resolve_getAllProfiles,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema_path = os.path.join(BASE_DIR, 'schema.graphql')

type_defs = gql(load_schema_from_path(schema_path))

query = QueryType()
mutation = MutationType()

# resolvers

query.set_field('getAllUsers', resolve_getAllUsers)
query.set_field('getUserById', resolve_getUserById)
query.set_field('getProfileByPublicId', resolve_getProfileByPublicId)
query.set_field('getAllProfiles', resolve_getAllProfiles)

schema = make_executable_schema(type_defs, query, mutation)