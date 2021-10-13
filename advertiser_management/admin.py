from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from .models import Ad, Advertiser, Click, View


class NameListFilter(SimpleListFilter):
    title = 'approved'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'approved'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """

        list_of_titles = [('all', 'Real All'),
                          (False, 'not approved'),
                          (True, 'approved')]
        return list_of_titles

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if str(self.value()) == 'all':
            return queryset

        return queryset.filter(approve__exact=self.value())


class AdAdmin(admin.ModelAdmin):
    list_filter = (NameListFilter,)
    search_fields = ['title']
    list_display = ['title', 'advertiser', 'approve']
    ordering = ['title']
    actions = ['make_approved']

    def make_approved(self, request, queryset):
        rows_updated = queryset.update(approve=True)
        if rows_updated == 1:
            message_bit = "1 ad was"
        else:
            message_bit = "%s ads were" % rows_updated
        self.message_user(request, "%s successfully marked as approved." % message_bit)

    make_approved.short_description = "Approve selected ads"


admin.site.register(Ad, AdAdmin)
admin.site.register(Advertiser)
admin.site.register(View)
admin.site.register(Click)
