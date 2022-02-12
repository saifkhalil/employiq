from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import candidate, certificate, education, employment
# Register your models here.


class EmployerResource(resources.ModelResource):
    class Meta:
        model: candidate
        fields = ('firstname', 'secondname', 'lastname', 'email', 'cv',
                  'birthofdate', 'phone_number', 'address1', 'city', 'country')


@register(candidate)
class CandidateAdmin(ImportExportModelAdmin):
    list_display = ('id', 'firstname', 'secondname', 'lastname', 'email', 'user', 'photo', 'cv',
                    'birthofdate', 'phone_number', 'address1', 'city', 'country', 'bio')
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
