from django.contrib import admin
from django.contrib.admin import ModelAdmin,register
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import candidate
# Register your models here.

class VendorResource(resources.ModelResource):
    class Meta:
        model : candidate
        fields  = ('firtname','secondname','lastname','photo','cv','birthofdate','phone_number','address','city','country','position','salary_desired','have_you_worked_here_before','have_you_applied_here_before','university','specility','skills','qualifications')


@register(candidate)
class CandidateAdmin(ImportExportModelAdmin):
    list_display = ('firtname','secondname','lastname','photo','cv','birthofdate','phone_number','address','city','country','position','salary_desired','have_you_worked_here_before','have_you_applied_here_before','university','specility','skills','qualifications')
    icon_name = 'assignment_ind'
