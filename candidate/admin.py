from django.contrib import admin
from django.contrib.admin import ModelAdmin,register
from .models import candidate
# Register your models here.
@register(candidate)
class CandidateAdmin(ModelAdmin):
    list_display = ('user','firtname','secondname','lastname','birthofdate','phone_number','address','city','country','position','salary_desired','have_you_worked_here_before','have_you_applied_here_before','college','skills','qualifications')
    icon_name = 'assignment_ind'