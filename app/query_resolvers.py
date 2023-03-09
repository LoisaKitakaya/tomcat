from app.models import Account, Category, Budget

# Category model query resolvers

def resolve_getAllCategories(*_):

    try:

        categories = Category.objects.all()

    except Exception as e:

        raise Exception(str(e))
    
    return categories

def resolve_getCategoryByPublicId(*_, public_id):

    try:

        category = Category.objects.filter(public_id=public_id).first()

    except Exception as e:

        raise Exception(str(e))
    
    return category

# Account model query resolvers

def resolve_getAllAccounts(*_):

    try:

        accounts = Account.objects.all()

    except Exception as e:

        raise Exception(str(e))
    
    return accounts

def resolve_getAccountByPublicId(*_, public_id):

    try:

        account = Account.objects.get(public_id=public_id)

    except Exception as e:

        raise Exception(str(e))
    
    return account

# Budget model query resolvers

def resolve_getAllBudgets(*_):

    try:

        budgets = Budget.objects.all()

    except Exception as e:

        raise Exception(str(e))
    
    return budgets

def resolve_getBudgetByPublicId(*_, public_id):

    try:

        budget = Budget.objects.filter(public_id=public_id).first()

    except Exception as e:

        raise Exception(str(e))
    
    return budget