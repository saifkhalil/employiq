from .models import candidate, education, employment
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
                  'start_date', 'end_date', 'job_title', 'supervisor_name', 'supervisor_title', 'supervisor_phone', 'supervisor_email',
                  'reason_for_leaving']
        widgets = {'country': CountrySelectWidget(
        ), 'start_date': DateInput(), 'end_date': DateInput()}


class CanForm(ModelForm):
    class Meta:
        model = candidate
        fields = ['title', 'firstname', 'secondname', 'lastname',
                  'email', 'alternate_email_address', 'phone_number', 'gender',
                  'photo', 'birthofdate', 'country_of_birth', 'place_of_birth', 'primary_nationality', 'secondary_nationality', 'highest_level_of_education', 'contact_phone', 'phone_type', 'address1', 'address2', 'city', 'country', 'postal_code', 'bio']
        widgets = {'country': CountrySelectWidget(
        ), 'start_date': DateInput(), 'end_date': DateInput()}
