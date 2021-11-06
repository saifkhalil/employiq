from django.contrib.admin import ModelAdmin,register
from .models import *
# Register your models here.
@register(vendor)
class VendorAdmin(ModelAdmin):
    list_display = ( 'company','phone_number','address','city','country')
    icon_name = 'business'

@register(job)
class JobAdmin(ModelAdmin):
    list_display = ('job_title', 'vendor','job_description','job_type','date_opened','date_closed','city','country','salary')
    icon_name = 'assignment'
    list_filter = ('job_title', 'vendor__company','job_type')
    list_select_related = ('vendor',)
