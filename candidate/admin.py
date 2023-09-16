import datetime
from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import candidate, certificate, education, employment, language
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.


class EmployerResource(resources.ModelResource):
    class Meta:
        model: candidate
        fields = ('firstname', 'secondname', 'lastname', 'email', 'cv',
                  'birthofdate', 'phone_number', 'address1', 'city', 'country')


@register(candidate)
class CandidateAdmin(ImportExportModelAdmin):
    # def photo_tag(self, obj):
    #     return format_html('<img src="{}" />'.format(obj.photo.url))
    
    # def image_tag(self, obj):
    #     return format_html('<img src="{}" width="auto" height="200px" />'.format(obj.photo.url))
        
    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.photo.url))
        
    image_tag.short_description = 'Image'
    
    list_display = ( 'id', 'firstname', 'secondname', 'lastname', 'email', 'user', 'photo', 'cv','birthofdate', 'phone_number', 'address1', 'city', 'country', 'bio')
    list_filter = ('email','user')
    icon_name = 'assignment_ind'


@register(education)
class EducationAdmin(ImportExportModelAdmin):
    list_display = ('id', 'education_level', 'country', 'city', 'institution',
                    'original_title_of_the_qualification', 'main_subject', 'start_date', 'graduation_date')
    icon_name = 'assignment_ind'


@register(employment)
class EmploymentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'employer', 'country', 'city', 'current_job',
                    'start_date', 'end_date', 'job_title', 'reason_for_leaving')
    icon_name = 'assignment_ind'


@register(certificate)
class CertificateAdmin(ImportExportModelAdmin):
    list_display = ('id', 'certificate_name', 'organization',
                    'issue_date', 'expire_date')
    icon_name = 'assignment_ind'


@register(language)
class LanguageAdmin(ImportExportModelAdmin):
    list_display = ('id', 'language', 'test', 'level', 'created',
                    'created_at', 'modified', 'modified_at')
    icon_name = 'assignment_ind'


@register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"