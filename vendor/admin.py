from django.contrib.admin import ModelAdmin,register
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *
# Register your models here.

class VendorResource(resources.ModelResource):
    class Meta:
        model : vendor
        fields  = ( 'company','is_subscribed','plan','subscription_from','subscription_to','remaining_records','phone_number','address','city','country',)


@register(vendor)
class VendorAdmin(ImportExportModelAdmin):
    list_display = ( 'company','is_subscribed','plan','subscription_from','subscription_to','remaining_records','phone_number','address','city','country')
    icon_name = 'business'

@register(job)
class JobAdmin(ModelAdmin):
    list_display = ('job_title', 'vendor','job_description','job_type','date_opened','date_closed','city','country','salary')
    icon_name = 'assignment'
    list_filter = ('job_title', 'vendor__company','job_type')
    list_select_related = ('vendor',)

@register(subscription_plan)
class PlanAdmin(ModelAdmin):
    list_display = ('id', 'plan','number_of_records')
    icon_name = 'assignment'
    list_filter = ('plan',)
