from django.shortcuts import render

from django.http import HttpResponse

from .models import Ad, Advertiser

def home(request):
    advertisers = Advertiser.objects.order_by('-clicks')

    return render(request, 'ads.html', {'advertisers': advertisers})


def inc_clicks(request, ad):
    return HttpResponse("inc_clicks %s" % ad)


def create_ad(request):
    return HttpResponse("some form to create new ad")