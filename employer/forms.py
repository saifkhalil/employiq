from .models import employer, job
from django.forms import DateInput, ModelForm
from django_countries.widgets import CountrySelectWidget
from django import forms
from django.utils.translation import ugettext_lazy as _
from tagify.fields import TagField
from ckeditor.widgets import CKEditorWidget


class EmpForm(ModelForm):
    class Meta:
        model = employer
        fields = ['company', 'logo', 'phone_number', 'public_company_info',
                  'communication_email', 'address', 'city',
                  'country']
        widgets = {'country': CountrySelectWidget()}


class JobForm(ModelForm):
    job_description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = job
        fields = ['job_title', 'job_description', 'job_type', 'city',
                  'country', 'salary', 'nationality',
                  'date_opened', 'date_closed']
        widgets = {'country': CountrySelectWidget(
        ), 'date_opened': DateInput(), 'date_closed': DateInput()}
