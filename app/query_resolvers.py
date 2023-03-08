from app.models import Account

# Account model query resolvers

def resolve_getAllAccounts(*_):

    try:

        accounts = Account.objects.all()

    except Exception as e:

        raise Exception(str(e))
    
    return accounts