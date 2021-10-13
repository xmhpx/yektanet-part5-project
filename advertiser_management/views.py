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

        delta = 0
        sz = 0.

        for clk in all_clicks:
            ad = clk.ad
            time = clk.datetime
            try:
                last_view = View.objects.filter(user_ip__exact=clk.user_ip, datetime__lte=time).order_by('-datetime')[0]
            except IndexError:
                last_view = clk
            td = time - last_view.datetime
            seconds = td.seconds + 86400 * td.days

            delta += seconds
            sz += 1.

        avg_delta = 'no clicks'
        if sz != 0:
            avg_delta = delta / sz

        click_per_time = {}
        view_per_time = {}

        for clk in all_clicks:
            time = clk.datetime.strftime("%d/%m/%Y %H")

            if time not in click_per_time:
                click_per_time[time] = 1
            else:
                click_per_time[time] += 1

        for viw in all_views:
            time = viw.datetime.strftime("%d/%m/%Y %H")

            if time not in view_per_time:
                view_per_time[time] = 1
            else:
                view_per_time[time] += 1

        click_per_view = {}
        for time in view_per_time:
            if time in click_per_time:
                click_per_view[time] = click_per_time[time] / view_per_time[time]
            else:
                click_per_view[time] = 'None'

        context['delta_time'] = datetime(2000, 1, 1, 3) - datetime(2000, 1, 1, 2)
        context['details_of_ad'] = details_of_ad
        context['avg_delta'] = avg_delta
        context['delta'] = delta
        context['sz'] = sz
        context['click_per_view'] = click_per_view

        return context
