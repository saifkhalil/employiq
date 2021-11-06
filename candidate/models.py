from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
import moneyed
from djmoney.models.fields import MoneyField
from accounts.models import User

User = settings.AUTH_USER_MODEL

class candidate(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firtname = models.CharField(max_length=200)
    secondname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    birthofdate = models.DateField()
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    country = CountryField(blank_label='(select country)')
    position  = models.CharField(max_length=200)
    salary_desired  = MoneyField(max_digits=10, decimal_places=3, default_currency='IQD')
    have_you_worked_here_before = models.BooleanField()
    have_you_applied_here_before = models.BooleanField()
    college = models.CharField(max_length=200)
    skills = models.TextField(max_length=1000)
    qualifications = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_createdby', on_delete=models.CASCADE,blank=True, null=True)
    modified_by = models.ForeignKey(User,related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.firtname + " " + self.secondname + " " + self.lastname

    def __unicode__(self):
       return self.firtname + " " + self.secondname + " " + self.lastname