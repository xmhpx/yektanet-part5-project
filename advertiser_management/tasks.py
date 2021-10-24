import time

from .models import *
from datetime import datetime, timedelta


def counter():
    now = datetime.now()
    click_cnt = {}
    view_cnt = {}
    for adv in Advertiser.object.all():
        view_cnt[adv.pk] = 0
        click_cnt[adv.pk] = 0

    for click in Click.object.all():
        if click.datetime > now - timedelta(hours=1):
            click_cnt[click.ad.advertiser.pk] += 1

    for view in View.object.all():
        if view.datetime > now - timedelta(hours=1):
            view_cnt[view.ad.advertiser.pk] += 1

    new_counter = Counter(starttime=now - timedelta(hours=1), endtime=now)

    new_counter.save()

    for adv in click_cnt:
        new_counter_value = CounterValue(counter=new_counter, advertiser=adv, click_cnt=click_cnt[adv.pk],
                                         view_cnt=view_cnt[adv.pk])
        new_counter_value.save()

    new_counter.save()

