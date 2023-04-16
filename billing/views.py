from users.models import User


def notifications(request):
    if request.method == "POST":
        pesapal_response = request.POST.dict()

        print(pesapal_response)
