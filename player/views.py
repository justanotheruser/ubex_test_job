from django.http import HttpResponse


def index(request):
    return HttpResponse("User home page")