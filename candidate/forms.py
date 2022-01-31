from .models import education, employment
from django.forms import ModelForm
from django_countries.widgets import CountrySelectWidget
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class EduForm(ModelForm):
    class Meta:
        model = education
        fields = ['education_level', 'country', 'city', 'institution',
                  'original_title_of_the_qualification', 'main_subject', 'start_date',
                  'graduation_date']
        widgets = {'country': CountrySelectWidget(
        ), 'start_date': DateInput(), 'graduation_date': DateInput()}


class EmpForm(ModelForm):
    class Meta:
        model = employment
        fields = ['employer', 'country', 'city', 'current_job',
                  'start_date', 'end_date', 'job_title',
                  'reason_for_leaving']
        widgets = {'country': CountrySelectWidget(
        ), 'start_date': DateInput(), 'end_date': DateInput()}
