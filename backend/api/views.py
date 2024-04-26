from django.shortcuts import render
from django.http import HttpResponse


def api_home(request, *args, **kwargs):
    return HttpResponse("This is the api landing page")