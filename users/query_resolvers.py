from users.models import User, Profile, UserLog, WorkSpace

# User model query resolvers

def resolve_getAllUsers(*_):

    try:

        all_users = User.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return all_users

def resolve_getUserById(*_, id):

    try:

        user = User.objects.get(id=id)

    except Exception as e:

        raise Exception(str(e))

    return user

def getUserByUsername(*_, username):

    try:

        user = User.objects.get(username=username)

    except Exception as e:

        raise Exception(str(e))
    
    return user

# Profile model query resolvers

def resolve_getAllProfiles(*_):

    try:

        profiles = Profile.objects.all()

    except Exception as e:

        raise Exception(str(e))
    
    return profiles

def resolve_getProfileById(*_, id):

    try:

        profile = Profile.objects.get(id=id)

    except Exception as e:

        raise Exception(str(e))
    
    return profile

# UserLog model query resolver

def resolve_getAllUserLogs(*_,):

    try:

        logs = UserLog.objects.all()

    except Exception as e:

        raise Exception(str(e))
    
    return logs

def resolve_getUserLogsByUserId(*_, id):

    try:

        user = User.objects.get(id=id)

        log = UserLog.objects.filter(user__id=user.id)

    except Exception as e:

        raise Exception(str(e))
    
    return log

# Workspace model query resolvers

def resolve_getWorkspaceById(*_, id):

    try:

        workspace = WorkSpace.objects.get(id=id)

    except Exception as e:

        raise Exception(str(e))
    
    return workspace