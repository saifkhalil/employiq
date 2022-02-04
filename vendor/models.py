from contextlib import nullcontext
from pyexpat import model
from django.db import models
from django.conf import settings
from django.forms import EmailField
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
import moneyed
from djmoney.models.fields import MoneyField
from easy_thumbnails.fields import ThumbnailerImageField
from accounts.models import User
from django.utils.translation import ugettext_lazy as _
User = settings.AUTH_USER_MODEL

NATIONALITY = [
    ('international', _('International')),
    ('national', _('National')),
    ('both', _('Both')),
]


class subscription_plan(models.Model):
    id = models.AutoField(primary_key=True)
    plan = models.CharField(max_length=200)
    number_of_records = models.IntegerField()

    def __str__(self):
        return self.plan

    def __unicode__(self):
        return self.plan


class vendor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('User'))
    company = models.CharField(max_length=200, verbose_name=_('Company Name'))
    logo = ThumbnailerImageField(
        upload_to='company_logos', blank=True, default='static/images/EIQLOGO.svg', verbose_name=_('Photo'))
    phone_number = PhoneNumberField(verbose_name=_('Phone Number'))
    public_company_info = models.BooleanField(
        default=False, verbose_name=_('Public company info'))
    communication_email = models.EmailField(
        null=False, blank=False, verbose_name=_('Communication Email'))
    address = models.CharField(max_length=500, verbose_name=_('Address'))
    city = models.CharField(max_length=500, verbose_name=_('City'))
    country = CountryField(blank_label=_(
        '(select country)'), verbose_name=_('Country'))
    is_subscribed = models.BooleanField(
        default=False, verbose_name=_('Is subscribed'))
    plan = models.ForeignKey(
        'subscription_plan', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Plan'))
    subscription_from = models.DateField(verbose_name=_('Subscription From'))
    subscription_to = models.DateField(verbose_name=_('Subscription To'))
    remaining_records = models.IntegerField(
        verbose_name=_('Remaining Records'))
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True)
    modified_by = models.ForeignKey(
        User, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.company

    def __unicode__(self):
        return self.company


class job(models.Model):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(vendor, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    job_description = models.CharField(max_length=200)
    job_type = models.CharField(max_length=200)
    date_opened = models.DateField()
    date_closed = models.DateField()
    city = models.CharField(max_length=200)
    country = CountryField(blank_label='(select country)')
    salary = MoneyField(max_digits=10, decimal_places=3,
                        default_currency='IQD')
    nationality = models.CharField(max_length=15, choices=NATIONALITY,
                                   default="both", blank=False, null=False, verbose_name=_('Nationality'))
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True)
    modified_by = models.ForeignKey(
        User, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title

    def __unicode__(self):
        return self.job_title
