from users.models import User, Profile
from ariadne_jwt.decorators import login_required

# User model mutation resolvers


def resolve_createUser(*_, username, email, first_name, last_name, password, password2):

    if not User.objects.filter(email=email).exists():

        if len(password) > 8 and len(password2) > 8:

            if password == password2:

                User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )

            else:

                raise Exception("Passwords provided did not match!")

            new_user = User.objects.get(email=email)

            new_user.set_password(password)

            new_user.save()

            Profile.objects.create(user=new_user)

        else:

            raise Exception("Password is too short. Must have minimum of 8 characters")

    else:

        raise Exception("Email already exists. Make sure your email is unique!")

    return new_user


@login_required
def resolve_updateUser(_, info, username, email, first_name, last_name):

    request = info.context["request"]

    if not User.objects.filter(email=email).exists():

        if not User.objects.filter(username=username).exists():

            user = User.objects.get(id=request.user.id)

            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            user.save()

        else:

            raise Exception(
                "Username already exists. Make sure your username is unique!"
            )

    else:

        raise Exception("Email already exists. Make sure your email is unique!")

    return user
