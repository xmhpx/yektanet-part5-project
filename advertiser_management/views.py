# from django.shortcuts import render

from django.http import HttpResponse


def home(request):
    return HttpResponse("ad ad ad ad")


def inc_clicks(request, ad):
    return HttpResponse("inc_clicks %s" % ad)


def create_ad(request):
    return HttpResponse("some form to create new ad")