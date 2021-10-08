from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect

from .models import Ad, Advertiser

def home(request):
    advertisers = Advertiser.objects.order_by('-clicks')

    for advertiser in advertisers:
        for ad in advertiser.ad_set.all():
            ad.views += 1
            ad.save()

    return render(request, 'ads.html', {'advertisers': advertisers})


def click(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    ad.clicks += 1
    ad.save()
    # output = "You clicked on %s" % ad
    # clcks = " now it has %s clicks" % ad.clicks
    # views = " and %s views" % ad.views
    return HttpResponseRedirect(ad.link)


def create_ad(request):
    return render(request, 'create_ad.html', {})