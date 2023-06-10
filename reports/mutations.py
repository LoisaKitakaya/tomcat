from uuid import uuid4
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from accounts.models import Account
from inventory.models import Product
from transactions.models import Transaction
from controls.cash_flow import GenerateCFReport
from controls.income import GenerateIncomeReport
from ariadne_jwt.decorators import login_required
from controls.balance_sheet import GenerateBSReport
from reports.models import (
    CashFlowRecord,
    IncomeStatement,
    CashFlowStatement,
    BalanceSheetStatement,
    CashFlowStatementIdentifier,
)


@login_required
def resolve_generateCashFlowReport(*_, account_id, begin_date: str, end_date: str):
    account = Account.objects.get(id=account_id)

    begin_date_object = datetime.strptime(begin_date, "%Y-%m-%dT%H:%M")
    begin_date_object = timezone.make_aware(
        begin_date_object, timezone.get_default_timezone()
    )

    end_date_object = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
    end_date_object = timezone.make_aware(
        end_date_object, timezone.get_default_timezone()
    )

    query = (
        Q(transaction_date__gte=begin_date_object)
        & Q(transaction_date__lte=end_date_object)
        & Q(account__id=account.pk)
    )

    try:
        transactions = Transaction.objects.filter(query).all()

    except Exception as e:
        raise Exception(str(e))

    cash_flow_object = GenerateCFReport(transactions)  # type: ignore

    grouped_data = cash_flow_object.group_transactions()

    reduced_data_set = []

    for data in grouped_data:
        reduced_data = cash_flow_object.reduce_data(data)

        reduced_data_set.append(reduced_data)

    cash_flow_object.cashflow_uid = str(uuid4().hex)

    for reduced_data in reduced_data_set:
        cash_flow_object.create_records(reduced_data)

    cash_flow_reports = CashFlowRecord.objects.filter(
        uid=cash_flow_object.cashflow_uid
    ).all()

    for report in cash_flow_reports:
        CashFlowStatement.objects.create(
            uid=cash_flow_object.cashflow_uid,
            account=account,
            record=report,
        )

    generated_report = CashFlowStatementIdentifier.objects.create(
        uid=cash_flow_object.cashflow_uid,
        account=account,
        period_start_date=begin_date_object,
        period_end_date=end_date_object,
    )

    return generated_report


@login_required
def resolve_deleteCashFlowReport(*_, uid: str):
    try:
        statement = CashFlowStatementIdentifier.objects.get(uid=uid)

        statement.delete()

    except Exception as e:
        raise Exception(str(e))

    try:
        report = CashFlowStatement.objects.filter(uid=uid).all()

        for item in report:
            item.delete()

    except Exception as e:
        raise Exception(str(e))

    try:
        records = CashFlowRecord.objects.filter(uid=uid).all()

        for record in records:
            record.delete()

    except Exception as e:
        raise Exception(str(e))

    return True


@login_required
def resolve_generateIncomeReport(*_, account_id, begin_date: str, end_date: str):
    account = Account.objects.get(id=account_id)

    begin_date_object = datetime.strptime(begin_date, "%Y-%m-%dT%H:%M")
    begin_date_object = timezone.make_aware(
        begin_date_object, timezone.get_default_timezone()
    )

    end_date_object = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
    end_date_object = timezone.make_aware(
        end_date_object, timezone.get_default_timezone()
    )

    query = (
        Q(transaction_date__gte=begin_date_object)
        & Q(transaction_date__lte=end_date_object)
        & Q(account__id=account.pk)
    )

    try:
        transactions = Transaction.objects.filter(query).all()

    except Exception as e:
        raise Exception(str(e))

    query = Q(account__id=account.pk)

    try:
        products = Product.objects.filter(query).all()

    except Exception as e:
        raise Exception(str(e))

    income_object = GenerateIncomeReport(transactions)  # type: ignore

    income_object.inventory_products = products  # type: ignore

    grouped_data = income_object.group_data()

    reduced_income_transactions = income_object.reduce_transaction_data(
        grouped_data["transaction_revenue"]
    )

    reduced_expense_transactions = income_object.reduce_transaction_data(
        grouped_data["operating_expense"]
    )

    total_revenue = income_object.get_total_revenue(reduced_income_transactions)

    if products:
        total_product_profit = income_object.get_total_product_profit(
            grouped_data["product_revenue"]
        )

    else:
        total_product_profit = 0.0

    gross_profit = income_object.get_gross_profit(total_revenue, total_product_profit)

    total_operation_expense = income_object.get_total_operation_expense(
        reduced_expense_transactions
    )

    net_income = income_object.get_net_income(gross_profit, total_operation_expense)

    income_object.income_uid = str(uuid4().hex)

    generated_report = IncomeStatement.objects.create(
        uid=income_object.income_uid,
        account=account,
        period_start_date=begin_date_object,
        period_end_date=end_date_object,
        revenue=total_revenue,
        gross_profit=gross_profit,
        operating_expenses=total_operation_expense,
        net_income=net_income,
    )

    return generated_report


@login_required
def resolve_deleteIncomeReport(*_, uid: str):
    try:
        report = IncomeStatement.objects.get(uid=uid)

        report.delete()

    except Exception as e:
        raise Exception(str(e))

    return True


@login_required
def resolve_generateBalanceSheetReport(
    *_, account_id, assets: list, liabilities: list, equity: list
):
    account = Account.objects.get(id=account_id)

    balance_sheet_object = GenerateBSReport(
        assets, liabilities, equity, account.account_balance
    )

    assets_net_worth = balance_sheet_object.process_assets()

    liabilities_net_worth = balance_sheet_object.process_liabilities()

    equity_net_worth = balance_sheet_object.process_equity(
        assets_net_worth, liabilities_net_worth
    )

    balance_sheet_object.balance_sheet_uid = str(uuid4().hex)

    generated_report = BalanceSheetStatement.objects.create(
        uid=balance_sheet_object.balance_sheet_uid,
        account=account,
        assets=assets_net_worth,
        liabilities=liabilities_net_worth,
        equity=equity_net_worth,
    )

    return generated_report


@login_required
def resolve_deleteBalanceSheetReport(*_, uid: str):
    try:
        report = BalanceSheetStatement.objects.get(uid=uid)

        report.delete()

    except Exception as e:
        raise Exception(str(e))

    return True
