from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
import moneyed
from djmoney.models.fields import MoneyField
from accounts.models import User

User = settings.AUTH_USER_MODEL

class vendor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    country = CountryField(blank_label='(select country)')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_createdby', on_delete=models.CASCADE,blank=True, null=True)
    modified_by = models.ForeignKey(User,related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE)

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
    salary = MoneyField(max_digits=10, decimal_places=3, default_currency='IQD')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_createdby', on_delete=models.CASCADE,blank=True, null=True)
    modified_by = models.ForeignKey(User,related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title

    def __unicode__(self):
        return self.job_title