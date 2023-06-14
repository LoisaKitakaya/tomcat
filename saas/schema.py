# schema.py
import os
import time

from ariadne import (
    QueryType,
    ScalarType,
    MutationType,
    make_executable_schema,
    load_schema_from_path,
)

from ariadne_jwt import (
    jwt_schema,
    GenericScalar,
    resolve_token_auth,
    resolve_refresh,
    resolve_verify,
)

from users.queries import *
from invoice.queries import *
from budgets.queries import *
from reports.queries import *
from users.mutations import *
from targets.queries import *
from controls.queries import *
from accounts.queries import *
from invoice.mutations import *
from reports.mutations import *
from budgets.mutations import *
from targets.mutations import *
from inventory.queries import *
from accounts.mutations import *
from inventory.mutations import *
from transactions.queries import *
from transactions.mutations import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema_path = os.path.join(BASE_DIR, "schema.graphql")

type_defs = load_schema_from_path(schema_path)

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

query.set_field("generateOTP", resolve_generateOTP)
query.set_field("generateQRCode", resolve_generateQRCode)

query.set_field("tokenAuth", resolve_token_auth)

query.set_field("getProductCategory", resolve_getProductCategory)
query.set_field("getProductSubCategory", resolve_getProductSubCategory)
query.set_field("getTransactionType", resolve_getTransactionType)
query.set_field("getTransactionCategory", resolve_getTransactionCategory)
query.set_field("getTransactionSubCategory", resolve_getTransactionSubCategory)

query.set_field("testProDecorator", resolve_testProDecorator)
query.set_field("testStandardDecorator", resolve_testStandardDecorator)

query.set_field("getUser", resolve_getUser)
query.set_field("getProfile", resolve_getProfile)
query.set_field("validateOrCreateUser", resolve_validateOrCreateUser)

query.set_field("getAllAccounts", resolve_getAllAccounts)
query.set_field("getAccount", resolve_getAccount)

query.set_field("getAllBudgets", resolve_getAllBudgets)
query.set_field("getBudget", resolve_getBudget)

query.set_field("getAllTargets", resolve_getAllTargets)
query.set_field("getTarget", resolve_getTarget)

query.set_field("getAllTransactions", resolve_getAllTransactions)
query.set_field("getTransaction", resolve_getTransaction)

query.set_field("getAllProducts", resolve_getAllProducts)
query.set_field("getProduct", resolve_getProduct)

query.set_field("getAllPaymentAccounts", resolve_getAllPaymentAccounts)
query.set_field("getPaymentAccount", resolve_getPaymentAccount)

query.set_field("getAllClientInformation", resolve_getAllClientInformation)
query.set_field("getClientInformation", resolve_getClientInformation)

query.set_field("getAllInvoices", resolve_getAllInvoices)
query.set_field("getInvoice", resolve_getInvoice)

query.set_field("getAllCashFlowStatements", resolve_getAllCashFlowStatements)
query.set_field("getCashFlowStatement", resolve_getCashFlowStatement)

query.set_field("getAllIncomeStatements", resolve_getAllIncomeStatements)
query.set_field("getIncomeStatement", resolve_getIncomeStatement)

query.set_field("getAllBalanceSheetStatements", resolve_getAllBalanceSheetStatements)
query.set_field("getBalanceSheetStatement", resolve_getBalanceSheetStatement)

# # mutation resolvers

mutation.set_field("createUser", resolve_createUser)
mutation.set_field("updateUser", resolve_updateUser)

mutation.set_field("verifyOTP", resolve_verifyOTP)

mutation.set_field("verifyToken", resolve_verify)
mutation.set_field("refreshToken", resolve_refresh)
mutation.set_field("tokenAuth", resolve_token_auth)

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

mutation.set_field("createProduct", resolve_createProduct)
mutation.set_field("updateProduct", resolve_updateProduct)
mutation.set_field("deleteProduct", resolve_deleteProduct)

mutation.set_field("createPaymentAccount", resolve_createPaymentAccount)
mutation.set_field("updatePaymentAccount", resolve_updatePaymentAccount)
mutation.set_field("deletePaymentAccount", resolve_deletePaymentAccount)

mutation.set_field("createClientInformation", resolve_createClientInformation)
mutation.set_field("updateClientInformation", resolve_updateClientInformation)
mutation.set_field("deleteClientInformation", resolve_deleteClientInformation)

mutation.set_field("createInvoice", resolve_createInvoice)
mutation.set_field("updateInvoice", resolve_updateInvoice)
mutation.set_field("deleteInvoice", resolve_deleteInvoice)

mutation.set_field("generateCashFlowReport", resolve_generateCashFlowReport)
mutation.set_field("deleteCashFlowReport", resolve_deleteCashFlowReport)

mutation.set_field("generateIncomeReport", resolve_generateIncomeReport)
mutation.set_field("deleteIncomeReport", resolve_deleteIncomeReport)

mutation.set_field("generateBalanceSheetReport", resolve_generateBalanceSheetReport)
mutation.set_field("deleteBalanceSheetReport", resolve_deleteBalanceSheetReport)

schema = make_executable_schema(
    [type_defs, jwt_schema],
    query,
    mutation,
    otp_scalar,
    qrcode_scalar,
    GenericScalar,
    datetime_scalar,
)
