from django.contrib.admin import ModelAdmin, register
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import employer, job, subscription_plan
# Register your models here.


class EmployerResource(resources.ModelResource):
    class Meta:
        model: employer
        fields = ('user', 'company', 'logo', 'public_company_info', 'communication_email', 'is_subscribed', 'plan',
                  'subscription_from', 'subscription_to', 'remaining_records', 'remaining_jobs', 'phone_number', 'address', 'city', 'country',)


class JobResource(resources.ModelResource):
    class Meta:
        model: job
        fields = ('job_title', 'employer', 'job_description', 'job_type',
                  'date_opened', 'date_closed', 'city', 'country', 'salary')


@register(employer)
class EmployerAdmin(ImportExportModelAdmin):
    list_display = ('user', 'company', 'is_verified', 'is_subscribed', 'plan', 'subscription_from',
                    'subscription_to', 'remaining_records', 'remaining_jobs', 'phone_number', 'address', 'city', 'country')
    icon_name = 'business'


@register(job)
class JobAdmin(ImportExportModelAdmin):
    list_display = ('job_title', 'employer', 'job_description', 'job_type',
                    'date_opened', 'date_closed', 'city', 'country', 'salary')
    icon_name = 'assignment'
    list_filter = ('job_title', 'employer__company', 'job_type')
    list_select_related = ('employer',)


@register(subscription_plan)
class PlanAdmin(ModelAdmin):
    list_display = ('id', 'plan', 'suggestions', 'jobs', 'price', 'days')
    icon_name = 'assignment'
    list_filter = ('plan',)
