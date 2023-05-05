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

from users.queries import *
from teams.queries import *
from teams.mutations import *
from budgets.queries import *
from users.mutations import *
from targets.queries import *
from controls.queries import *
from accounts.queries import *
from billing.mutations import *
from budgets.mutations import *
from targets.mutations import *
from inventory.queries import *
from accounts.mutations import *
from inventory.mutations import *
from transactions.queries import *
from transactions.mutations import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema_path = os.path.join(BASE_DIR, "schema.graphql")

type_defs = gql(load_schema_from_path(schema_path))

# scaler types

datetime_scalar = ScalarType("Datetime")
otp_scalar = ScalarType("Otp")
qrcode_scalar = ScalarType("Qrcode")


@datetime_scalar.serializer
def serialize_datetime(value):
    timestamp = str(time.mktime(value.timetuple()))

    return timestamp


@otp_scalar.serializer
def serialize_otp(value):
    if len(value) == 2 and value[1] == "test":
        return {
            "success": True,
            "otp_code": value[0],
            "message": "A One-Time-Password has been sent to your email address.",
        }

    else:
        return {
            "success": True,
            "message": "A One-Time-Password has been sent to your email address.",
        }


@qrcode_scalar.serializer
def serialize_qrcode(value):
    return value


# query and mutation types

query = QueryType()
mutation = MutationType()

# resolvers

# # query resolvers

# # # user app query resolvers

query.set_field("generateOTP", resolve_generateOTP)
query.set_field("generateQRCode", resolve_generateQRCode)

query.set_field("getTransactionType", resolve_getTransactionType)
query.set_field("getTransactionCategory", resolve_getTransactionCategory)
query.set_field("getTransactionSubCategory", resolve_getTransactionSubCategory)
query.set_field("getProductCategory", resolve_getProductCategory)
query.set_field("getProductSubCategory", resolve_getProductSubCategory)

query.set_field("testStandardDecorator", resolve_testStandardDecorator)
query.set_field("testProDecorator", resolve_testProDecorator)
query.set_field("testIfIsEmployee", resolve_testIfIsEmployee)

query.set_field("getUser", resolve_getUser)
query.set_field("getProfile", resolve_getProfile)

# # # app app query resolvers

query.set_field("getAllAccounts", resolve_getAllAccounts)
query.set_field("getAccount", resolve_getAccount)

query.set_field("getAllBudgets", resolve_getAllBudgets)
query.set_field("getBudget", resolve_getBudget)

query.set_field("getAllTargets", resolve_getAllTargets)
query.set_field("getTarget", resolve_getTarget)

query.set_field("getAllTransactions", resolve_getAllTransactions)
query.set_field("getTransaction", resolve_getTransaction)

query.set_field("getWorkspace", resolve_getWorkspace)
query.set_field("getTeamLogs", resolve_getTeamLogs)
query.set_field("getTeamMembers", resolve_getTeamMembers)

query.set_field("getAllProducts", resolve_getAllProducts)
query.set_field("getProduct", resolve_getProduct)

# # mutation resolvers

# # # user model mutation resolvers

mutation.set_field("createUser", resolve_createUser)
mutation.set_field("updateUser", resolve_updateUser)

# # # authentication mutation resolvers

mutation.set_field("verifyOTP", resolve_verifyOTP)

mutation.set_field("verifyToken", resolve_verify)
mutation.set_field("refreshToken", resolve_refresh)
mutation.set_field("tokenAuth", resolve_token_auth)

# # # app models mutation resolvers

mutation.set_field("createAccount", resolve_createAccount)
mutation.set_field("updateAccount", resolve_updateAccount)
mutation.set_field("deleteAccount", resolve_deleteAccount)

mutation.set_field("createBudget", resolve_createBudget)
mutation.set_field("updateBudget", resolve_updateBudget)
mutation.set_field("budgetStatus", resolve_budgetStatus)
mutation.set_field("deleteBudget", resolve_deleteBudget)

mutation.set_field("createTarget", resolve_createTarget)
mutation.set_field("updateTarget", resolve_updateTarget)
mutation.set_field("targetStatus", resolve_targetStatus)
mutation.set_field("deleteTarget", resolve_deleteTarget)

mutation.set_field("createTransaction", resolve_createTransaction)
mutation.set_field("updateTransaction", resolve_updateTransaction)
mutation.set_field("deleteTransaction", resolve_deleteTransaction)

mutation.set_field("updateWorkspace", resolve_updateWorkspace)

mutation.set_field("createTeamMember", resolve_createTeamMember)
mutation.set_field("deleteTeamMember", resolve_deleteTeamMember)

mutation.set_field("subscribeToPlan", resolve_subscribeToPlan)

mutation.set_field("createProduct", resolve_createProduct)
mutation.set_field("updateProduct", resolve_updateProduct)
mutation.set_field("deleteProduct", resolve_deleteProduct)

schema = make_executable_schema(
    [type_defs, jwt_schema],
    query,
    mutation,
    otp_scalar,
    qrcode_scalar,
    GenericScalar,
    datetime_scalar,
)
