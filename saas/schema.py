# schema.py
import os
from ariadne import QueryType, MutationType, make_executable_schema, load_schema_from_path, gql

# app models
from users.models import User

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema_path = os.path.join(BASE_DIR, 'schema.graphql')

type_defs = gql(load_schema_from_path(schema_path))

query = QueryType()
mutation = MutationType()

# resolvers

@query.field('getAllUsers')
def resolve_getAllUsers(*_):

    try:

        all_users = User.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return all_users

@query.field('getUserById')
def resolve_getUserById(*_, id):

    try:

        user = User.objects.get(id=id)

    except Exception as e:

        raise Exception(str(e))

    return user

@query.field('getUserByUsername')
def getUserByUsername(*_, username):

    try:

        user = User.objects.get(username=username)

    except Exception as e:

        raise Exception(str(e))
    
    return user

schema = make_executable_schema(type_defs, query, mutation)