from django.contrib.admin import ModelAdmin, register
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import employer, job, subscription_features, subscription_plan, Transaction, Subscription, suggestion
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
    list_filter = ('company',)


@register(job)
class JobAdmin(ImportExportModelAdmin):
    list_display = ('job_title', 'employer', 'job_description', 'job_type',
                    'date_opened', 'date_closed', 'city', 'country', 'salary')
    icon_name = 'assignment'
    list_filter = ('job_title', 'employer__company', 'job_type')
    list_select_related = ('employer',)


@register(subscription_features)
class FeaturesAdmin(ModelAdmin):
    list_display = ('id', 'feature', )
    icon_name = 'assignment'
    list_filter = ('feature',)


@register(subscription_plan)
class PlanAdmin(ModelAdmin):
    list_display = ('id', 'plan', 'suggestions', 'jobs',
                    'price', 'days', 'features_list', 'is_active')
    icon_name = 'assignment'
    list_filter = ('plan',)

    def features_list(self, obj):
        return [feature.feature for feature in obj.features.all()]


@register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = ('id', 'employer', 'subscription', 'amount',
                    'payment_status', 'transaction_id')
    icon_name = 'assignment'
    list_filter = ('employer',)


@register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_display = ('id', 'employer', 'plan', 'used_jobs',
                    'remaining_jobs', 'used_suggestions', 'remaining_suggestions', 'start_date', 'end_date', 'is_active')
    icon_name = 'assignment'
    list_filter = ('plan', 'employer')


@register(suggestion)
class suggestionAdmin(ModelAdmin):
    list_display = ('id', 'employer', 'candidate', 'created_at')
    icon_name = 'assignment'
    list_filter = ('employer',)
