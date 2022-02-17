from .models import employer, job
from django.forms import CheckboxInput, DateInput, ModelForm
from django_countries.widgets import CountrySelectWidget
from django import forms
from django.utils.translation import ugettext_lazy as _
from tagify.fields import TagField
from ckeditor.widgets import CKEditorWidget


class EmpForm(ModelForm):
    class Meta:
        model = employer
        fields = ['company', 'industry', 'logo', 'phone_number', 'public_company_info',
                  'communication_email', 'address', 'city',
                  'country']
        widgets = {'country': CountrySelectWidget()}


class DateInput(forms.DateInput):
    input_type = 'date'


class JobForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['country'].disabled = True

    class Meta:
        model = job
        fields = ['job_title', 'job_description', 'job_type', 'city',
                  'country', 'salary', 'nationality',
                  'date_opened', 'date_closed']
        widgets = {'country': CountrySelectWidget(
        ), 'date_opened': DateInput(), 'date_closed': DateInput(), 'job_description': CKEditorWidget()}
