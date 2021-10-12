from datetime import datetime

from django.shortcuts import render, get_object_or_404, reverse

from django.http import HttpResponseRedirect

from .models import Ad, Advertiser, View, Click


def home(request):
    try:
        advertiser_id = request.POST['advertiser_id']
        advertiser = Advertiser.objects.get(pk=advertiser_id)
        title = request.POST['title']
        imgUrl = request.POST['image_url']
        link = request.POST['link']
        new_ad = Ad(title=title, imgUrl=imgUrl, link=link, advertiser=advertiser)
        new_ad.save()
        advertiser.save()

        return HttpResponseRedirect(reverse('home'))

    except Advertiser.DoesNotExist:
        return render(request, 'create_ad.html', {
            'error_message': "Advertiser id does not exist.",
        })

    except KeyError:
        pass

    advertisers = Advertiser.objects.all()
    user_ip = request.META['REMOTE_ADDR']

    for advertiser in advertisers:
        for ad in advertiser.ad_set.all():
            new_view = View(ad=ad, user_ip=user_ip, datetime=datetime.now())
            new_view.save()
            advertiser.views += 1
        advertiser.save()

    return render(request, 'ads.html', {'advertisers': advertisers})


def click(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    user_ip = request.META['REMOTE_ADDR']

    new_click = Click(ad=ad, user_ip=user_ip, datetime=datetime.now())
    new_click.save()

    ad.advertiser.clicks += 1
    ad.advertiser.save()

    # output = "You clicked on %s" % ad
    # clcks = " now it has %s clicks" % ad.clicks
    # views = " and %s views" % ad.views

    return HttpResponseRedirect(ad.link)


def create_ad(request):
    return render(request, 'create_ad.html', {})
