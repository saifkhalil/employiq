from .models import employer, job, Subscription
from django.forms import CheckboxInput, DateInput, ModelForm
from django_countries.widgets import CountrySelectWidget
from django import forms
from django.utils.translation import ugettext_lazy as _
from tagify.fields import TagField
from ckeditor.widgets import CKEditorWidget


class EmpForm(ModelForm):
    class Meta:
        model = employer
        fields = ['company', 'industry', 'logo', 'phone_number', 'website', 'public_company_info',
                  'communication_email', 'address', 'city',
                  'country']
        widgets = {'country': CountrySelectWidget()}


class DateInput(forms.DateInput):
    input_type = 'date'


class JobForm(ModelForm):
    keywords = TagField(label=_('Position keywords'),
                        help_text="Press Enter ( ↵ ) to add new keyword", delimiters=',')

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['country'].disabled = True

    class Meta:
        model = job
        fields = ['job_title', 'keywords', 'job_description', 'job_type', 'city',
                  'country', 'salary', 'nationality',
                  'date_opened', 'date_closed']
        widgets = {'country': CountrySelectWidget(
        ), 'date_opened': DateInput(), 'date_closed': DateInput(), 'job_description': CKEditorWidget()}


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ['employer', 'plan', 'start_date']
        widgets = {'start_date': DateInput(), }
