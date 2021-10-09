from django.shortcuts import render, get_object_or_404, reverse

from django.http import HttpResponseRedirect

from .models import Ad, Advertiser


def home(request):
    try:
        advertiser = Advertiser.objects.get(pk=request.POST['advertiser_id'])
        title = request.POST['title']
        imgUrl = request.POST['image_url']
        link = request.POST['link']
        new_ad = Ad(title=title, imgUrl=imgUrl, link=link, advertiser=advertiser)
        new_ad.save()
        advertiser.save()

        advertisers = Advertiser.objects.order_by('-clicks')

        for advertiser in advertisers:
            for ad in advertiser.ad_set.all():
                ad.views += 1
                advertiser.views += 1
                ad.save()
            advertiser.save()

        return HttpResponseRedirect(reverse('home'))

    except(KeyError, Advertiser.DoesNotExist):
        pass

    advertisers = Advertiser.objects.order_by('-clicks')

    for advertiser in advertisers:
        for ad in advertiser.ad_set.all():
            ad.views += 1
            advertiser.views += 1
            ad.save()
        advertiser.save()

    return render(request, 'ads.html', {'advertisers': advertisers})




def click(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    ad.clicks += 1
    ad.advertiser.clicks += 1
    ad.advertiser.save()
    ad.save()
    # output = "You clicked on %s" % ad
    # clcks = " now it has %s clicks" % ad.clicks
    # views = " and %s views" % ad.views
    return HttpResponseRedirect(ad.link)


def create_ad(request):
    return render(request, 'create_ad.html', {})
