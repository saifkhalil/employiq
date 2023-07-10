from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
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
from tagify.models import TagField
User = settings.AUTH_USER_MODEL

TITLE_CHOICES = [
    ('MR', _('Mr.')),
    ('MS', _('Ms.')),
    ('MRS', _('Mrs.')),
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

GOVERNORATES = [
    ('Al Anbar', _('Al Anbar')),
    ('Babylon', _('Babylon')),
    ('Baghdad', _('Baghdad')),
    ('Basra', _('Basra')),
    ('Dhi Qar', _('Dhi Qar')),
    ('Al-Qadisiyyah', _('Al-Qadisiyyah')),
    ('Diyala', _('Diyala')),
    ('Duhok', _('Duhok')),
    ('Erbil', _('Erbil')),
    ('Halabja', _('Halabja')),
    ('Karbala', _('Karbala')),
    ('Kirkuk', _('Kirkuk')),
    ('Maysan', _('Maysan')),
    ('Muthanna', _('Muthanna')),
    ('Najaf', _('Najaf')),
    ('Nineveh', _('Nineveh')),
    ('Saladin', _('Saladin')),
    ('Sulaymaniyah', _('Sulaymaniyah')),
    ('Wasit', _('Wasit')),
    ('None (not residing in Iraq)', _('None (not residing in Iraq)')),

]


class employment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    employer = models.CharField(
        max_length=50, blank=False, null=False, verbose_name=_('Employer'))
    employer_industry = models.CharField(
        max_length=50, blank=False, null=False, verbose_name=_('Employer Industry'))
    country = CountryField(blank=False, null=False, verbose_name=_('Country'))
    city = models.CharField(blank=False, null=False,
                            max_length=500, verbose_name=_('City'))
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

    class Meta:
        ordering = ('-start_date',)


class language(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    language = LanguageField(max_length=10, blank=False,
                             null=False)
    level = models.CharField(
        max_length=10, choices=LANGUAGE_LEVELS, blank=False, null=False, verbose_name=_('Level'))
    test = models.CharField(max_length=200, null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    created = models.ForeignKey(
        User, related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True, editable=False)
    modified = models.ForeignKey(
        User, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):

        if not self.id:
            self.created_by = get_current_authenticated_user
            self.modified_by = get_current_authenticated_user
            self.test = get_current_authenticated_user
            super(language, self).save(*args, **kwargs)
        elif self.id:

            self.modified_by = get_current_authenticated_user
            self.modified_at = datetime.datetime.now()
            self.test = get_current_user
            super(language, self).save(*args, **kwargs)


# @receiver(post_save, sender=language, dispatch_uid="add_to_candidate")
# def add_to_candidate(sender, instance, **kwargs):
#     current_candidate = instance.create_by
#     instance.candidate_set = current_candidate
#     instance.product.save()


class education(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    education_level = models.CharField(
        max_length=1, choices=EDUCATION_CHOICES, blank=False, null=False, verbose_name=_('Education Level'))
    country = CountryField(blank=False, null=False, verbose_name=_('Country'))
    city = models.CharField(blank=False, null=False,
                            max_length=500, verbose_name=_('City'))
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

    class Meta:
        ordering = ('-start_date',)


class certificate(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    certificate_name = models.CharField(
        max_length=100,  blank=False, null=False, verbose_name=_('Certificate Name'))
    organization = models.CharField(max_length=50, blank=True,
                                    null=True, verbose_name=_('Organization'))
    issue_date = models.DateField(
        blank=True, null=True, verbose_name=_('Issue Date'))
    expire_date = models.DateField(
        blank=True, null=True, verbose_name=_('Expire Date'))
    expired_certificate = models.CharField(
        max_length=1, default='N', choices=JOB_CHOICES, blank=False, null=False, verbose_name=_('This credential does not expire'))
    attach = models.FileField(blank=True, null=True,
                              upload_to='media/certificate', verbose_name=_('Attach File'), validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'git'])])

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = ('-issue_date',)


class candidate(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES,
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
        blank=False, null=False, verbose_name=_('Country of Birth'))
    place_of_birth = models.CharField(
        max_length=200, blank=False, null=False, verbose_name=_('Place of birth'))
    primary_nationality = CountryField(
        blank=False, null=False, verbose_name=_('Primary nationality'))
    secondary_nationality = CountryField(
        blank=True, null=True, verbose_name=_('Seondary nationality'))
    highest_level_of_education = models.CharField(
        max_length=1, choices=EDUCATION_CHOICES, blank=False, null=False, verbose_name=_('Highest level of education'))
    contact_phone = PhoneNumberField(verbose_name=_('Conact phone'))
    phone_type = models.CharField(blank=True, null=True,
                                  max_length=1, choices=PHONE_CHOICES, verbose_name=_('Type'))
    alternate_email_address = models.EmailField(blank=True, null=True,
                                                verbose_name=_('Alternative email address'))
    address1 = models.CharField(
        max_length=500, verbose_name=_('Current address Line(1)'))
    address2 = models.CharField(
        blank=True, null=True, max_length=500, verbose_name=_('Address Line(2)'))
    city = models.CharField(max_length=500, default='Baghdad',
                            choices=GOVERNORATES, verbose_name=_('Current City'))
    country = CountryField(
        blank_label=_('(select country)'), verbose_name=_('Current country'))
    postal_code = models.IntegerField(validators=[MaxValueValidator(
        99999), MinValueValidator(10000)], verbose_name=_('Postal Code'), blank=True, null=True)
    education = models.ManyToManyField(
        'education', blank=True, verbose_name=_('Candidate Education'))
    certificate = models.ManyToManyField(
        'certificate', blank=True, verbose_name=_('Certificates'))
    Employment = models.ManyToManyField(
        'employment', blank=True, verbose_name=_('Employment History'))
    language = models.ManyToManyField(
        'language', blank=True, verbose_name=_('Language Skills'))
    cv = models.FileField(upload_to='media/cv',
                          verbose_name=_('CV File'), blank=True, null=True)
    bio = models.CharField(max_length=1000, blank=True,
                           null=True, verbose_name=_('bio / About you'))
    skills = TagField(verbose_name=_('Skills'), delimiters=',')
    hobbies = TagField(verbose_name=_('Hobbies'), delimiters=',')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        User, related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True, editable=False)
    modified_by = models.ForeignKey(
        User, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.firstname + " " + self.secondname + " " + self.lastname

    def __unicode__(self):
        return self.firstname + " " + self.secondname + " " + self.lastname

    class Meta:
        unique_together = ('id', 'user','email',)
        ordering = ('-created_at',)
