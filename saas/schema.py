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
    resolve_getAllProfiles
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema_path = os.path.join(BASE_DIR, 'schema.graphql')

type_defs = gql(load_schema_from_path(schema_path))

# scaler types

datetime_scalar = ScalarType("Datetime")
image_scalar = ScalarType("Image")

@datetime_scalar.serializer
def serialize_datetime(value):

    date = time.mktime(value.timetuple())

    return str(date)

@image_scalar.serializer
def serialize_image(value):

    return value.url

# query and mutation types

query = QueryType()
mutation = MutationType()

# resolvers

query.set_field('getAllUsers', resolve_getAllUsers)
query.set_field('getUserByPublicId', resolve_getUserByPublicId)
query.set_field('getUserByUsername', resolve_getUserByUsername)

query.set_field('getAllProfiles', resolve_getAllProfiles)
query.set_field('getProfileByPublicId', resolve_getProfileByPublicId)

schema = make_executable_schema(
    type_defs,[
    query, 
    mutation,
    datetime_scalar,
    image_scalar
    ]
)