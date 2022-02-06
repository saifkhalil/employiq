from tabnanny import verbose
from django.utils.translation import ugettext_lazy as _
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
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, FileExtensionValidator
from PIL import Image
from django.core.files.base import ContentFile
from easy_thumbnails.fields import ThumbnailerImageField
from languages.fields import LanguageField
User = settings.AUTH_USER_MODEL

TITLE_CHOICES = [
    ('MR', _('Mr.')),
    ('MS', _('Ms.')),
]

GENDER_CHOICES = [
    ('F', _('Female')),
    ('M', _('Male')),
]


PHONE_CHOICES = [
    ('H', _('Home')),
    ('M', _('Mobile')),
    ('W', _('Work')),
]

JOB_CHOICES = [
    ('Y', _('Yes')),
    ('N', _('No')),
]

MARITAL_STATUS = [
    ('Single', _('Single')),
    ('Married', _('Married')),
    ('Widowed', _('Widowed')),
    ('Separated', _('Separated')),
    ('Divorced', _('Divorced')),
]

EDUCATION_CHOICES = [
    ('1', _('Non-Degree Programme')),
    ('2', _('High School diploma')),
    ('3', _('Technical Diploma')),
    ('4', _('Bachelors Degree')),
    ('5', _('Master Degree')),
    ('6', _('PhD Doctorate Degree')),
]

LANGUAGE_LEVELS = [
    ('1', _('Beginner')),
    ('2', _('Professional communication')),
    ('3', _('Fluent')),
    ('4', _('Mother tongue')),
]


class employment(models.Model):
    id = models.AutoField(primary_key=True)
    employer = models.CharField(
        max_length=50, blank=False, null=False, verbose_name=_('Employer'))
    country = CountryField(blank=False, null=False, verbose_name=_('Country'))
    city = models.CharField(max_length=50, blank=False,
                            null=False, verbose_name=_('City'))
    current_job = models.CharField(
        max_length=1, default='N', choices=JOB_CHOICES, blank=False, null=False, verbose_name=_('Current Job'))
    start_date = models.DateField(
        blank=False, null=False, verbose_name=_('Start Date'))
    end_date = models.DateField(
        blank=True, null=True, verbose_name=_('End Date'))
    job_title = models.CharField(
        max_length=50, blank=False, null=False, verbose_name=_('Job Title'))
    job_description = models.CharField(
        max_length=2000, validators=[MinLengthValidator(200)], blank=False, null=False, verbose_name=_('Job Description'))
    reason_for_leaving = models.CharField(
        max_length=200, blank=True, null=True, verbose_name=_('Reason for leaving'))
    supervisor_name = models.CharField(
        max_length=50, blank=False, null=False, verbose_name=_("Supervisor's Name"))
    supervisor_title = models.CharField(
        max_length=50, blank=False, null=False, verbose_name=_("Supervisor's Title"))
    supervisor_phone = PhoneNumberField(
        blank=False, null=False, verbose_name=_("Supervisor's Phone"))
    supervisor_email = models.EmailField(
        max_length=100, blank=False, null=False, verbose_name=_("Supervisor's Email"))

    def __str__(self):
        return self.employer

    def __unicode__(self):
        return self.employer


class language(models.Model):
    id = models.AutoField(primary_key=True)
    language = LanguageField(max_length=10, blank=False,
                             null=False)
    level = models.CharField(
        max_length=10, choices=LANGUAGE_LEVELS, blank=False, null=False, verbose_name=_('Level'))

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)


class education(models.Model):
    id = models.AutoField(primary_key=True)
    education_level = models.CharField(
        max_length=1, choices=EDUCATION_CHOICES, blank=False, null=False, verbose_name=_('Education Level'))
    country = CountryField(blank=False, null=False, verbose_name=_('Country'))
    city = models.CharField(max_length=50, blank=False,
                            null=False, verbose_name=_('City'))
    institution = models.CharField(
        max_length=100, blank=False, null=False, verbose_name=_('Institution'))
    original_title_of_the_qualification = models.CharField(
        max_length=100, blank=False, null=False, verbose_name=_('Original Title of the qualification'))
    main_subject = models.CharField(
        max_length=100, blank=False, null=False, verbose_name=_('Main subject'))
    start_date = models.DateField(
        blank=False, null=False, verbose_name=_('Start Date'))
    graduation_date = models.DateField(
        blank=False, null=False, verbose_name=_('Graduation Date'))

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)


class candidate(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=2, choices=TITLE_CHOICES,
                             default="Mr.", blank=False, null=False, verbose_name=_('Title'))
    firstname = models.CharField(
        max_length=200, blank=False, null=False, verbose_name=_('First Name'))
    secondname = models.CharField(
        max_length=200, blank=False, null=False, verbose_name=_('Second Name'))
    lastname = models.CharField(
        max_length=200, blank=False, null=False, verbose_name=_('Last Name'))
    email = models.EmailField(
        max_length=200, blank=False, null=False, verbose_name=_('Email'))
    phone_number = PhoneNumberField(
        blank=False, null=False, verbose_name=_('Phone'))
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES,
                              default="M", blank=False, null=False, verbose_name=_('Gender'))
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS,
                                      default="Single", blank=False, null=False, verbose_name=_('Marital Status'))
    photo = ThumbnailerImageField(
        upload_to='photos', blank=True, default='photos/default.jpg', verbose_name=_('Photo'))
    birthofdate = models.DateField(
        blank=False, null=False, verbose_name=_('Birth of date'))
    country_of_birth = CountryField(
        blank=False, null=False, verbose_name=_('Country'))
    place_of_birth = models.CharField(
        max_length=200, blank=False, null=False, verbose_name=_('Place of birth'))
    primary_nationality = CountryField(
        blank=False, null=False, verbose_name=_('Primary nationality'))
    secondary_nationality = CountryField(
        blank=True, null=True, verbose_name=_('Seondary nationality'))
    highest_level_of_education = models.CharField(
        max_length=1, choices=EDUCATION_CHOICES, blank=False, null=False, verbose_name=_('Highest level of education'))
    contact_phone = PhoneNumberField(
        blank=True, null=True, verbose_name=_('Conact phone'))
    phone_type = models.CharField(blank=True, null=True,
                                  max_length=1, choices=PHONE_CHOICES, verbose_name=_('Type'))
    alternate_email_address = models.EmailField(blank=True, null=True,
                                                verbose_name=_('Alternative email address'))
    address1 = models.CharField(
        max_length=500, verbose_name=_('Address Line(1)'))
    address2 = models.CharField(
        blank=True, null=True, max_length=500, verbose_name=_('Address Line(2)'))
    city = models.CharField(max_length=500, verbose_name=_('City'))
    country = CountryField(
        blank_label=_('(select country)'), verbose_name=_('Country'))
    postal_code = models.IntegerField(validators=[MaxValueValidator(
        99999), MinValueValidator(10000)], verbose_name=_('Postal Code'))
    education = models.ManyToManyField(
        'education', blank=True, verbose_name=_('Candidate Education'))
    Employment = models.ManyToManyField(
        'employment', blank=True, verbose_name=_('Employment History'))
    language = models.ManyToManyField(
        'language', blank=True, verbose_name=_('Language Skills'))
    cv = models.FileField(upload_to='media/cv', verbose_name=_('CV File'))
    bio = models.CharField(max_length=1000, blank=True,
                           null=True, verbose_name=_('bio'))
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
