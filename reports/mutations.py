from uuid import uuid4
from datetime import datetime
from django.db.models import Q
from users.models import Profile
from django.utils import timezone
from accounts.models import Account
from transactions.models import Transaction
from teams.models import Workspace, TeamLogs
from reports.cash_flow import GenerateCFReport
from ariadne_jwt.decorators import login_required
from reports.models import CashFlowStatement, CashFlowRecord


@login_required
def resolve_generateReport(_, info, account_id, begin_date, end_date):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    begin_date_object = datetime.strptime(begin_date, "%Y-%m-%dT%H:%M")
    begin_date_object = timezone.make_aware(
        begin_date_object, timezone.get_default_timezone()
    )

    end_date_object = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
    end_date_object = timezone.make_aware(
        end_date_object, timezone.get_default_timezone()
    )

    new_report = CashFlowStatement.objects.create(
        account=account,
        statement_uid=str(uuid4().hex),
        begin_date=begin_date_object,
        end_date=end_date_object,
    )

    query = Q(transaction_date__gte=begin_date_object) & Q(
        transaction_date__lte=end_date_object
    )

    try:
        transactions = Transaction.objects.filter(query).all()

    except Exception as e:
        raise Exception(str(e))

    report_object = GenerateCFReport(transactions)

    grouped_data = report_object.group_transactions()

    reduced_operating_inflow = GenerateCFReport.reduce_data(
        grouped_data["Operating Inflow"]
    )
    reduced_operating_outflow = GenerateCFReport.reduce_data(
        grouped_data["Operating Outflow"]
    )

    reduced_investing_inflow = GenerateCFReport.reduce_data(
        grouped_data["Investing Inflow"]
    )
    reduced_investing_outflow = GenerateCFReport.reduce_data(
        grouped_data["Investing Outflow"]
    )

    reduced_financing_inflow = GenerateCFReport.reduce_data(
        grouped_data["Financing Inflow"]
    )
    reduced_financing_outflow = GenerateCFReport.reduce_data(
        grouped_data["Financing Outflow"]
    )

    GenerateCFReport.create_records(new_report.statement_uid, reduced_operating_inflow)
    GenerateCFReport.create_records(new_report.statement_uid, reduced_operating_outflow)

    GenerateCFReport.create_records(new_report.statement_uid, reduced_investing_inflow)
    GenerateCFReport.create_records(new_report.statement_uid, reduced_investing_outflow)

    GenerateCFReport.create_records(new_report.statement_uid, reduced_financing_inflow)
    GenerateCFReport.create_records(new_report.statement_uid, reduced_financing_outflow)

    generated_report = CashFlowRecord.objects.filter(
        statement_uid=new_report.statement_uid
    ).all()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"created report: {new_report.statement_uid}",
        )

    return generated_report


@login_required
def resolve_deleteReport(_, info, statement_uid):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    try:
        reports = CashFlowRecord.objects.filter(statement_uid=statement_uid).all()

        report_name = statement_uid

        for report in reports:
            report.delete()

    except Exception as e:
        raise Exception(str(e))

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted report: {report_name}",
        )

    return True
