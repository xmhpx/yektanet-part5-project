import time

from .models import *
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404


def counter():
    now = datetime.now()
    click_cnt = {}
    view_cnt = {}
    for adv in Advertiser.objects.all():
        view_cnt[adv.pk] = 0
        click_cnt[adv.pk] = 0

    for click in Click.objects.all():
        if click.datetime.replace(tzinfo=None) > now - timedelta(hours=1):
            click_cnt[click.ad.advertiser.pk] += 1

    for view in View.objects.all():
        if view.datetime.replace(tzinfo=None) > now - timedelta(hours=1):
            view_cnt[view.ad.advertiser.pk] += 1

    new_counter = Counter(starttime=now - timedelta(hours=1), endtime=now)

    new_counter.save()

    for pk in click_cnt:
        new_counter_value = CounterValue(counter=new_counter, advertiser=get_object_or_404(Advertiser, pk=pk), click_cnt=click_cnt[pk],
                                         view_cnt=view_cnt[pk])
        new_counter_value.save()

    new_counter.save()

    return new_counter.pk
