from uuid import uuid4
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

            new_user.public_id = str(uuid4().hex)

            new_user.set_password(password)

            new_user.save()

        else:

            raise Exception(
                "Password is too short. Must have minimum of 8 characters"
            )

    else:

        raise Exception(
            "Email already exists. Make sure your email is unique!"
        )
    
    return new_user
