from datetime import datetime

from django.views.generic.base import TemplateView

from django.shortcuts import render, get_object_or_404, reverse

from django.http import HttpResponseRedirect, Http404

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
            if ad.approve:
                new_view = View(ad=ad, user_ip=user_ip, datetime=datetime.now())
                new_view.save()
                advertiser.views += 1
        advertiser.save()

    return render(request, 'ads.html', {'advertisers': advertisers})


def click(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)

    if not ad.approve:
        raise Http404

    user_ip = request.META['REMOTE_ADDR']

    new_click = Click(ad=ad, user_ip=user_ip, datetime=datetime.now())
    new_click.save()

    ad.advertiser.clicks += 1
    ad.advertiser.save()

    # output = "You clicked on %s" % ad
    # clicks = " now it has %s clicks" % ad.clicks
    # views = " and %s views" % ad.views

    return HttpResponseRedirect(ad.link)


class CreateAdView(TemplateView):
    template_name = "create_ad.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DetailView(TemplateView):
    template_name = "detail.html"
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_ads = Ad.objects.filter(approve__exact=True)
        all_clicks = Click.objects.filter(ad__approve__exact=True)
        all_views = View.objects.filter(ad__approve__exact=True)

        details_of_ad = {}

        for clk in all_clicks:
            ad = clk.ad
            time = clk.datetime.strftime('%m/%d/%Y : %H')

            if ad not in details_of_ad:
                details_of_ad[ad] = {}

            if time not in details_of_ad[ad]:
                details_of_ad[ad][time] = {'click': 0, 'view': 0}

            details_of_ad[ad][time]['click'] += 1

        for viw in all_views:
            ad = viw.ad
            time = viw.datetime.strftime('%m/%d/%Y : %H')

            if ad not in details_of_ad:
                details_of_ad[ad] = {}

            if time not in details_of_ad[ad]:
                details_of_ad[ad][time] = {'click': 0, 'view': 0}

            details_of_ad[ad][time]['view'] += 1

        context['details_of_ad'] = details_of_ad

        return context
