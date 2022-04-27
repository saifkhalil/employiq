from .models import candidate, education, employment, language, certificate
from django.forms import ModelForm
from django_countries.widgets import CountrySelectWidget
from django import forms
from django.utils.translation import ugettext_lazy as _
from tagify.fields import TagField
from ckeditor.widgets import CKEditorWidget
from bootstrap_modal_forms.forms import BSModalModelForm
from phonenumber_field.formfields import PhoneNumberField

from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget, PhoneNumberPrefixWidget


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
    job_description = forms.CharField(widget=CKEditorWidget(
    ), help_text="Word limit 200, Explain more about your duties")

    class Meta:
        model = employment
        fields = ['employer', 'employer_industry', 'country', 'city', 'current_job',
                  'start_date', 'end_date', 'job_title', 'job_description', 'supervisor_name', 'supervisor_title', 'supervisor_phone', 'supervisor_email',
                  'reason_for_leaving']
        widgets = {'country': CountrySelectWidget(
        ), 'start_date': DateInput(), 'end_date': DateInput()}


class LangForm(ModelForm):
    class Meta:
        model = language
        fields = ['language', 'level']


class CerForm(ModelForm):
    class Meta:
        model = certificate
        fields = ['certificate_name', 'organization',
                  'issue_date', 'expire_date', 'expired_certificate', 'attach']
        widgets = {'issue_date': DateInput(), 'expire_date': DateInput()}


class CanForm(ModelForm):
    skills = TagField(label=_('Skills'), place_holder=_(
        'add a skills'), delimiters=' ')
    hobbies = TagField(label=_('Hobbies'), place_holder=_(
        'add a hobbies'), delimiters=' ')
#     phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IQ'))
# 	phone_number.error_messages['invalid'] = 'Enter a valid phone number (e.g. +9647801000000).'

    class Meta:
        model = candidate
        fields = ['title', 'firstname', 'secondname', 'lastname',
                  'email', 'alternate_email_address', 'phone_number', 'gender',  'marital_status',
                  'photo', 'birthofdate', 'country_of_birth', 'place_of_birth', 'primary_nationality', 'secondary_nationality', 'highest_level_of_education', 'contact_phone', 'phone_type', 'address1', 'address2', 'city', 'country', 'postal_code', 'bio', 'skills', 'hobbies']
        widgets = {'country': CountrySelectWidget(
        ), 'start_date': DateInput(), 'end_date': DateInput(), 'birthofdate': DateInput()}
