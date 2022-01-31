from io import BytesIO
import os.path
from django.db import models
from django.conf import settings
from django.db.models.fields import BooleanField
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
import moneyed
from djmoney.models.fields import MoneyField
#from pkg_resources import Version
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
from django.core.files.base import ContentFile
from easy_thumbnails.fields import ThumbnailerImageField
User = settings.AUTH_USER_MODEL

TITLE_CHOICES = [
    ('MR', 'Mr.'),
    ('MS', 'Ms.'),
]

GENDER_CHOICES = [
    ('F', 'Female'),
    ('M', 'Male'),
]


PHONE_CHOICES = [
    ('H', 'Home'),
    ('M', 'Mobile'),
    ('W', 'Work'),
]

JOB_CHOICES = [
    ('Y', 'Yes'),
    ('N', 'No'),
]

EDUCATION_CHOICES = [
    ('1', 'Non-Degree Programme'),
    ('2', 'High School diploma'),
    ('3', 'Technical Diploma'),
    ('4', 'Bachelors Degree'),
    ('5', 'Master Degree'),
    ('6', 'PhD Doctorate Degree'),
]


class employment(models.Model):
    id = models.AutoField(primary_key=True)
    employer = models.CharField(
        max_length=50, blank=False, null=False, verbose_name='Employer')
    country = CountryField(blank=False, null=False, verbose_name='Country')
    city = models.CharField(max_length=50, blank=False,
                            null=False, verbose_name='City')
    current_job = models.CharField(
        max_length=1, default='N', choices=JOB_CHOICES, blank=False, null=False, verbose_name='Current Job')
    start_date = models.DateField(
        blank=False, null=False, verbose_name='Start Date')
    end_date = models.DateField(blank=True, null=True, verbose_name='End Date')
    job_title = models.CharField(
        max_length=50, blank=False, null=False, verbose_name='Job Title')
    reason_for_leaving = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Reason for leaving')

    def __str__(self):
        return self.employer

    def __unicode__(self):
        return self.employer


class education(models.Model):
    id = models.AutoField(primary_key=True)
    education_level = models.CharField(
        max_length=1, choices=EDUCATION_CHOICES, blank=False, null=False, verbose_name='Education Level')
    country = CountryField(blank=False, null=False, verbose_name='Country')
    city = models.CharField(max_length=50, blank=False,
                            null=False, verbose_name='City')
    institution = models.CharField(
        max_length=100, blank=False, null=False, verbose_name='Institution')
    original_title_of_the_qualification = models.CharField(
        max_length=100, blank=False, null=False, verbose_name='Original Title of the qualification')
    main_subject = models.CharField(
        max_length=100, blank=False, null=False, verbose_name='Main subject')
    start_date = models.DateField(
        blank=False, null=False, verbose_name='Start Date')
    graduation_date = models.DateField(
        blank=False, null=False, verbose_name='Graduation Date')

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)


class candidate(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=2, choices=TITLE_CHOICES,
                             default="Mr.", blank=False, null=False, verbose_name='Title')
    firstname = models.CharField(
        max_length=200, blank=False, null=False, verbose_name='First Name')
    secondname = models.CharField(
        max_length=200, blank=False, null=False, verbose_name='Second Name')
    lastname = models.CharField(
        max_length=200, blank=False, null=False, verbose_name='Last Name')
    email = models.EmailField(
        max_length=200, blank=False, null=False, verbose_name='Email')
    phone_number = PhoneNumberField(
        blank=False, null=False, verbose_name='Phone')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES,
                              default="M", blank=False, null=False, verbose_name='Gender')
    photo = ThumbnailerImageField(
        upload_to='photos', blank=True, default='photos/default.jpg')
    birthofdate = models.DateField(
        blank=False, null=False, verbose_name='Birth of date')
    country_of_birth = CountryField(
        blank=False, null=False, verbose_name='Country')
    place_of_birth = models.CharField(
        max_length=200, blank=False, null=False, verbose_name='Place of birth')
    primary_nationality = CountryField(
        blank=False, null=False, verbose_name='Primary nationality')
    secondary_nationality = CountryField(
        blank=True, null=True, verbose_name='Seondary nationality')
    highest_level_of_education = models.CharField(
        max_length=1, choices=EDUCATION_CHOICES, blank=False, null=False, verbose_name='Highest level of education')
    contact_phone = PhoneNumberField(
        blank=True, null=True, verbose_name='Conact phone')
    phone_type = models.CharField(blank=True, null=True,
                                  max_length=1, choices=PHONE_CHOICES, verbose_name='Type')
    alternate_email_address = models.EmailField(blank=True, null=True,
                                                verbose_name='Alternative email address')
    address1 = models.CharField(max_length=500, verbose_name='Address Line(1)')
    address2 = models.CharField(
        blank=True, null=True, max_length=500, verbose_name='Address Line(2)')
    city = models.CharField(max_length=500, verbose_name='City')
    country = CountryField(
        blank_label='(select country)', verbose_name='Country')
    postal_code = models.IntegerField(validators=[MaxValueValidator(
        99999), MinValueValidator(10000)], verbose_name='Postal Code')
    education = models.ManyToManyField(
        'education', blank=True, verbose_name='Candidate Education')
    Employment = models.ManyToManyField(
        'employment', blank=True, verbose_name='Employment History')
    cv = models.FileField(upload_to='media/cv', verbose_name='CV File')
    bio = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True)
    modified_by = models.ForeignKey(
        User, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname + " " + self.secondname + " " + self.lastname

    def __unicode__(self):
        return self.firstname + " " + self.secondname + " " + self.lastname
