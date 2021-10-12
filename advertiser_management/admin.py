from django.contrib import admin

from .models import Ad, Advertiser, Click, View

admin.site.register(Ad)
admin.site.register(Advertiser)
admin.site.register(View)
admin.site.register(Click)