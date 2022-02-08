from .models import vendor, job
from django.forms import DateInput, ModelForm
from django_countries.widgets import CountrySelectWidget
from django import forms
from django.utils.translation import ugettext_lazy as _
from tagify.fields import TagField


class EmpForm(ModelForm):
    class Meta:
        model = vendor
        fields = ['company', 'logo', 'phone_number', 'public_company_info',
                  'communication_email', 'address', 'city',
                  'country']
        widgets = {'country': CountrySelectWidget()}


class JobForm(ModelForm):
    class Meta:
        model = job
        fields = ['job_title', 'job_description', 'job_type', 'city',
                  'country', 'salary', 'nationality',
                  'date_opened', 'date_closed']
        widgets = {'country': CountrySelectWidget(
        ), 'date_opened': DateInput(), 'date_closed': DateInput()}
