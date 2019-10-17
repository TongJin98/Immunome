from django.http import HttpResponse


def index(request):
    return HttpResponse("Anchors Generator for Human Vaccine Project")
