from ariadne_jwt.decorators import login_required
from reports.models import CashFlowRecord, CashFlowStatement


@login_required
def resolve_getAllReports(*_, account_id):
    all_reports = CashFlowStatement.objects.filter(account__id=account_id)

    return all_reports


@login_required
def resolve_getReport(*_, statement_uid):
    try:
        records = CashFlowRecord.objects.filter(statement_uid=statement_uid).all()

    except Exception as e:
        raise Exception(str(e))

    else:
        return records
