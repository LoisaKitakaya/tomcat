from users.models import User, Profile
from ariadne_jwt.decorators import login_required

# User model query resolvers


@login_required
def resolve_getAllUsers(*_):

    try:

        all_users = User.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return all_users


@login_required
def resolve_getUserByPublicId(*_, public_id):

    try:

        user = User.objects.get(public_id=public_id)

    except Exception as e:

        raise Exception(str(e))

    return user


@login_required
def resolve_getUserByUsername(*_, username):

    try:

        user = User.objects.get(username=username)

    except Exception as e:

        raise Exception(str(e))

    return user


# Profile model query resolvers


@login_required
def resolve_getAllProfiles(*_):

    try:

        profiles = Profile.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return profiles


@login_required
def resolve_getProfileByPublicId(*_, public_id):

    try:

        profile = Profile.objects.get(public_id=public_id)

    except Exception as e:

        raise Exception(str(e))

    return profile
