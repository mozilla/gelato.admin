#from django import forms
from django.conf import settings
from django.contrib import admin
from gelato.constants.base import (MARKETPLACE_TYPES, ADDON_SEARCH_TYPES,
                                   ADDON_PERSONA, ADDON_PLUGIN)
from gelato.models import addons, versions, applications

#XXX move to gelato.constants
def get_addon_search_types():
    types = ADDON_SEARCH_TYPES[:]
    if not settings.SEARCH_EXCLUDE_PERSONAS:
        types.append(ADDON_PERSONA)
    return types


def get_admin_search_types():
    types = get_addon_search_types()
    types.append(ADDON_PLUGIN)
    return types



class AddonAdmin(admin.ModelAdmin):
    exclude = ('authors',)
    list_display = ('__unicode__', 'type', 'status', 'average_rating',
                    'premium_type', 'premium')
    list_filter = ('type', 'status')

    fieldsets = (
        (None, {
            'fields': ('name', 'guid', 'default_locale', 'type', 'status',
                       'highest_status', 'outstanding'),
        }),
        ('Details', {
            'fields': ('summary', 'description', 'homepage', 'eula',
                       'privacy_policy', 'developer_comments', 'icon_type',
                       'the_reason', 'the_future'),
        }),
        ('Support', {
            'fields': ('support_url', 'support_email',
                       'get_satisfaction_company', 'get_satisfaction_product'),
        }),
        ('Stats', {
            'fields': ('average_rating', 'bayesian_rating', 'total_reviews',
                       'weekly_downloads', 'total_downloads',
                       'average_daily_downloads', 'average_daily_users',
                       'share_count'),
        }),
        ('Truthiness', {
            'fields': ('disabled_by_user', 'trusted', 'view_source',
                       'public_stats', 'prerelease', 'admin_review',
                       'site_specific', 'external_software', 'dev_agreement'),
        }),
        ('Money', {
            'fields': ('wants_contributions', 'paypal_id', 'suggested_amount',
                       'annoying'),
        }),
        ('Dictionaries', {
            'fields': ('target_locale', 'locale_disambiguation'),
        }))

    def queryset(self, request):
        types = (MARKETPLACE_TYPES if settings.MARKETPLACE else
                 get_admin_search_types())
        return addons.AddonBase.objects.filter(type__in=types)


class FeatureAdmin(admin.ModelAdmin):
    raw_id_fields = ('addon',)
    list_filter = ('application', 'locale')
    list_display = ('addon', 'application', 'locale')


class CategoryAdmin(admin.ModelAdmin):
    raw_id_fields = ('addons',)
    list_display = ('name', 'application', 'type', 'count')
    list_filter = ('application', 'type')
    exclude = ('count',)


class FrozenAddonAdmin(admin.ModelAdmin):
    raw_id_fields = ('addon',)



class AppVersionAdmin(admin.StackedInline):
    model = applications.AppVersion
    ordering = ('-version_int',)


class ApplicationAdmin(admin.ModelAdmin):
    inlines = [AppVersionAdmin]



# class CompatOverrideRangeInline(admin.TabularInline):
#     model = models.CompatOverrideRange
#     # Exclude type since firefox only supports blocking right now.
#     exclude = ('type',)


# class CompatOverrideAdminForm(forms.ModelForm):

#     def clean(self):
#         if '_confirm' in self.data:
#             raise forms.ValidationError('Click "Save" to confirm changes.')
#         return self.cleaned_data


# class CompatOverrideAdmin(admin.ModelAdmin):
#     raw_id_fields = ('addon',)
#     inlines = [CompatOverrideRangeInline]
#     form = CompatOverrideAdminForm


def register():
    # admin.site.register(models.BlacklistedGuid)
    # admin.site.register(models.Feature, FeatureAdmin)
    admin.site.register(addons.Category, CategoryAdmin)
    admin.site.register(addons.AddonBase, AddonAdmin)
    # admin.site.register(models.FrozenAddon, FrozenAddonAdmin)
    # admin.site.register(models.CompatOverride, CompatOverrideAdmin)

    admin.site.register(versions.VersionBase)

    admin.site.register(applications.Application, ApplicationAdmin)

