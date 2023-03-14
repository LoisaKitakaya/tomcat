# schema.py
import os
import time

from ariadne import (
    QueryType,
    ScalarType,
    MutationType,
    make_executable_schema,
    load_schema_from_path,
    gql,
)

from ariadne_jwt import (
    jwt_schema,
    GenericScalar,
    resolve_token_auth,
    resolve_refresh,
    resolve_verify,
)

from users.query_resolvers import *
from users.mutation_resolvers import *
from app.query_resolvers import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema_path = os.path.join(BASE_DIR, "schema.graphql")

type_defs = gql(load_schema_from_path(schema_path))

# scaler types

datetime_scalar = ScalarType("Datetime")


@datetime_scalar.serializer
def serialize_datetime(value):

    timestamp = str(time.mktime(value.timetuple()))

    return timestamp


# query and mutation types

query = QueryType()
mutation = MutationType()

# resolvers

# # query resolvers

# # # user app query resolvers

query.set_field("getAllUsers", resolve_getAllUsers)
query.set_field("getUser", resolve_getUser)
query.set_field("getUserByUsername", resolve_getUserByUsername)

query.set_field("getAllProfiles", resolve_getAllProfiles)
query.set_field("getProfile", resolve_getProfile)

# # # app app query resolvers

query.set_field("getAllCategories", resolve_getAllCategories)
query.set_field("getCategoryByPublicId", resolve_getCategoryByPublicId)

query.set_field("getAllAccounts", resolve_getAllAccounts)
query.set_field("getAccount", resolve_getAccount)

query.set_field("getAllBudgets", resolve_getAllBudgets)
query.set_field("getBudget", resolve_getBudget)

query.set_field("getAllTransactions", resolve_getAllTransactions)
query.set_field("getTransaction", resolve_getTransaction)

query.set_field("getAllReports", resolve_getAllReports)
query.set_field("getReport", resolve_getReport)

# # mutation resolvers

# # # user model mutation resolvers

mutation.set_field("createUser", resolve_createUser)
mutation.set_field("updateUser", resolve_updateUser)

# # # authentication mutation resolvers

mutation.set_field("verifyToken", resolve_verify)
mutation.set_field("refreshToken", resolve_refresh)
mutation.set_field("tokenAuth", resolve_token_auth)

schema = make_executable_schema(
    [type_defs, jwt_schema],
    query,
    mutation,
    GenericScalar,
    datetime_scalar,
)
