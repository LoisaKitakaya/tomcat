from ariadne_jwt.decorators import login_required
from reports.models import (
    IncomeStatement,
    CashFlowStatement,
    BalanceSheetStatement,
    CashFlowStatementIdentifier,
)


@login_required
def resolve_getAllCashFlowStatements(*_, account_id):
    try:
        cash_flow_statements = CashFlowStatementIdentifier.objects.filter(
            account__id=account_id
        ).all()

    except Exception as e:
        raise Exception(str(e))

    return cash_flow_statements


@login_required
def resolve_getCashFlowStatement(*_, uid: str):
    try:
        cash_flow_statements = CashFlowStatement.objects.filter(uid=uid).all()

    except Exception as e:
        raise Exception(str(e))

    return cash_flow_statements


@login_required
def resolve_getAllIncomeStatements(*_, account_id):
    try:
        income_statements = IncomeStatement.objects.filter(account__id=account_id).all()

    except Exception as e:
        raise Exception(str(e))

    return income_statements


@login_required
def resolve_getIncomeStatement(*_, uid: str):
    try:
        income_statement = IncomeStatement.objects.get(uid=uid)

    except Exception as e:
        raise Exception(str(e))

    return income_statement


@login_required
def resolve_getAllBalanceSheetStatements(*_, account_id):
    try:
        balance_sheet_statements = BalanceSheetStatement.objects.filter(account__id=account_id).all()

    except Exception as e:
        raise Exception(str(e))

    return balance_sheet_statements


@login_required
def resolve_getBalanceSheetStatement(*_, uid: str):
    try:
        balance_sheet_statement = BalanceSheetStatement.objects.get(uid=uid)

    except Exception as e:
        raise Exception(str(e))

    return balance_sheet_statement
