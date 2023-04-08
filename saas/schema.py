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
from app.mutation_resolvers import *
from teams.query_resolvers import *
from teams.mutation_resolvers import *
from billing.query_resolvers import *
from billing.mutation_resolvers import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema_path = os.path.join(BASE_DIR, "schema.graphql")

type_defs = gql(load_schema_from_path(schema_path))

# scaler types

datetime_scalar = ScalarType("Datetime")
date_scalar = ScalarType("Date")
number_scalar = ScalarType("Number")
time_scalar = ScalarType("Time")
otp_scalar = ScalarType("Otp")
qrcode_scalar = ScalarType("Qrcode")


@datetime_scalar.serializer
def serialize_datetime(value):

    timestamp = str(time.mktime(value.timetuple()))

    return timestamp


@date_scalar.serializer
def serialize_date(value):

    date = value.isoformat()

    return date


@number_scalar.serializer
def serialize_number(value):

    number = "{:,}".format(value)

    return number


@time_scalar.serializer
def serialize_time(value):

    date = value.strftime("%Y-%m-%d")

    return date


@otp_scalar.serializer
def serialize_otp(value):

    return value


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

query.set_field("getAllUsers", resolve_getAllUsers)
query.set_field("getUser", resolve_getUser)
query.set_field("getUserByUsername", resolve_getUserByUsername)

query.set_field("getAllProfiles", resolve_getAllProfiles)
query.set_field("getProfile", resolve_getProfile)

# # # app app query resolvers

query.set_field("getAllAccounts", resolve_getAllAccounts)
query.set_field("getAccount", resolve_getAccount)

query.set_field("getAllBudgets", resolve_getAllBudgets)
query.set_field("getBudget", resolve_getBudget)

query.set_field("getAllTargets", resolve_getAllTargets)
query.set_field("getTarget", resolve_getTarget)

query.set_field("getAllTransactions", resolve_getAllTransactions)
query.set_field("getTransactionsByAccount", resolve_getTransactionsByAccount)
query.set_field("getTransaction", resolve_getTransaction)

query.set_field("getWorkspace", resolve_getWorkspace)
query.set_field("getTeamLogs", resolve_getTeamLogs)
query.set_field("getTeamMembers", resolve_getTeamMembers)

query.set_field("getAllCardUsers", resolve_getAllCardUsers)
query.set_field("getCardUser", resolve_getCardUser)

query.set_field("getAllMpesaUsers", resolve_getAllMpesaUsers)
query.set_field("getMpesaUser", resolve_getMpesaUser)

query.set_field("getAllCardPayments", resolve_getAllCardPayments)
query.set_field("getUserCardPayments", resolve_getUserCardPayments)

query.set_field("getAllMpesaPayments", resolve_getAllMpesaPayments)
query.set_field("getUserMpesaPayments", resolve_getUserMpesaPayments)

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

mutation.set_field("registerCard", resolve_registerCard)
mutation.set_field("registerAndBillCard", resolve_registerAndBillCard)

mutation.set_field("registerMpesa", resolve_registerMpesa)
mutation.set_field("registerAndBillMpesa", resolve_registerAndBillMpesa)

mutation.set_field("requestBilling", resolve_requestBilling)
mutation.set_field("cancelPlan", resolve_cancelPlan)

schema = make_executable_schema(
    [type_defs, jwt_schema],
    query,
    mutation,
    otp_scalar,
    date_scalar,
    time_scalar,
    qrcode_scalar,
    GenericScalar,
    number_scalar,
    datetime_scalar,
)
