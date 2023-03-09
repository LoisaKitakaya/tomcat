from users.models import User, Profile

# User model query resolvers


def resolve_getAllUsers(*_):

    try:

        all_users = User.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return all_users


def resolve_getUserByPublicId(*_, public_id):

    try:

        user = User.objects.get(public_id=public_id)

    except Exception as e:

        raise Exception(str(e))

    return user


def resolve_getUserByUsername(*_, username):

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


def resolve_getProfileByPublicId(*_, public_id):

    try:

        profile = Profile.objects.get(public_id=public_id)

    except Exception as e:

        raise Exception(str(e))

    return profile
