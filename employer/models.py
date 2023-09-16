from datetime import datetime
from tagify.models import TagField
from ast import keyword
from email.policy import default
from candidate.models import candidate
import uuid
from ckeditor.fields import RichTextField
from pyexpat import model
from django.db import models
from django.conf import settings
from django.forms import EmailField
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from easy_thumbnails.fields import ThumbnailerImageField
from accounts.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

User = settings.AUTH_USER_MODEL
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

NATIONALITY = [
    ('international', _('International')),
    ('national', _('National')),
    ('both', _('Both')),
]

BOOL_CHOICES = [
    ('Y', _('Yes')),
    ('N', _('No')),
]

Employment_Type = [
    ('Full-time', _('Full-time')),
    ('Part-time', _('Part-time')),
    ('Service contract', _('Service contract')),
    ('Temporary', _('Temporary')),
    ('Volunteer', _('Volunteer')),
    ('Internship', _('Internship')),
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

]


class subscription_plan(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.CharField(max_length=200, verbose_name=_('plan'))
    suggestions = models.IntegerField(verbose_name=_('suggestions'))
    jobs = models.IntegerField(verbose_name=_('Jobs'))
    price = models.IntegerField(verbose_name=_('Price'))
    days = models.IntegerField()
    active = models.BooleanField(
        default=True,
        help_text=_('whether this plan list is active or not.'),
    )

    def __str__(self):
        return self.plan

    def __unicode__(self):
        return self.plan


def validate_image(image):
    width, height = get_image_dimensions(image)
    if height != width:
        raise ValidationError(
            _("Please select logo with scale 1:1 (square) and maximum height and width is 300px"))
    if height >= 301:
        raise ValidationError(
            _("Please select logo with scale 1:1 (square) and maximum height and width is 300px"))


class employer(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('User'))
    company = models.CharField(max_length=200, verbose_name=_('Company Name'))
    logo = ThumbnailerImageField(
        upload_to='company_logos', blank=False, null=False, verbose_name=_('Logo'))
    industry = models.CharField(max_length=200, verbose_name=_('industry'))
    phone_number = PhoneNumberField(verbose_name=_('Phone Number'))
    public_company_info = models.CharField(max_length=10, choices=BOOL_CHOICES, default='Yes',
                                           verbose_name=_('Make company info public? (logo and name)'))
    communication_email = models.EmailField(
        null=False, blank=False, verbose_name=_('Email for receiving CVs'))
    website = models.URLField(blank=True, null=True,
                              max_length=200, verbose_name=_('website'))
    address = models.CharField(max_length=500, verbose_name=_('Address'))
    city = models.CharField(max_length=500, default='Baghdad',
                            choices=GOVERNORATES, verbose_name=_('City'))
    country = CountryField(default='IQ', blank_label=_(
        '(select country)'), verbose_name=_('Country'))
    is_subscribed = models.BooleanField(
        default=False, verbose_name=_('Is subscribed'))
    plan = models.ForeignKey(
        'subscription_plan', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Plan'))
    subscription_from = models.DateField(
        blank=True, null=True, verbose_name=_('Subscription From'))
    subscription_to = models.DateField(
        blank=True, null=True, verbose_name=_('Subscription To'))
    remaining_records = models.IntegerField(blank=True, null=True,
                                            verbose_name=_('Remaining Records'), default=0)
    remaining_jobs = models.IntegerField(blank=True, null=True,
                                         verbose_name=_('Remaining Jobs'))
    is_verified = models.BooleanField(default=False, blank=False, null=False)
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

    class Meta:
        unique_together = ('id', 'user',)


#
# class employer_subscription(models.Model):
#     id = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False)
#     employer = models.ForeignKey(employer, on_delete=models.CASCADE)
#     plan = models.ForeignKey(subscription_plan, on_delete=models.CASCADE)
#     date_billing_start = models.DateTimeField(
#         blank=True,
#         help_text=_('the date to start billing this subscription'),
#         null=True,
#         verbose_name='billing start date',
#     )
#     date_billing_end = models.DateTimeField(
#         blank=True,
#         help_text=_('the date to finish billing this subscription'),
#         null=True,
#         verbose_name='billing start end',
#     )
#     date_billing_last = models.DateTimeField(
#         blank=True,
#         help_text=_('the last date this plan was billed'),
#         null=True,
#         verbose_name='last billing date',
#     )
#     date_billing_next = models.DateTimeField(
#         blank=True,
#         help_text=_('the next date billing is due'),
#         null=True,
#         verbose_name='next start date',
#     )
#     active = models.BooleanField(
#         default=True,
#         help_text=_('whether this subscription is active or not'),
#     )
#     cancelled = models.BooleanField(
#         default=False,
#         help_text=_('whether this subscription is cancelled or not'),
#     )
#     used_suggestions = models.IntegerField(verbose_name=_('Used suggestions'),default=0)
#     used_jobs = models.IntegerField(verbose_name=_('Used jobs'),default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         User, related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True)
#     modified_by = models.ForeignKey(
#         User, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.id)
#
#     def __unicode__(self):
#         return str(self.id)
#
#     def remaining_jobs(self):
#         return int(self.plan.jobs - self.used_jobs) if self.plan.jobs is not None and self.used_jobs is not None else 0
#
#     def remaining_suggestions(self):
#         return int(self.plan.suggestions - self.used_suggestions) if self.plan.suggestions is not None and self.used_suggestions is not None else 0
# class SubscriptionTransaction(models.Model):
#     """Details for a subscription plan billing."""
#     id = models.UUIDField(
#         default=uuid.uuid4,
#         editable=False,
#         primary_key=True,
#         verbose_name='ID',
#     )
#     employer = models.ForeignKey(
#         employer,
#         help_text=_('the employer that this subscription was billed for'),
#         null=True,
#         on_delete=models.SET_NULL,
#         related_name='subscription_transactions'
#     )
#     subscription = models.ForeignKey(
#         subscription_plan,
#         help_text=_('the plan costs that were billed'),
#         null=True,
#         on_delete=models.SET_NULL,
#         related_name='transactions'
#     )
#     date_transaction = models.DateTimeField(
#         help_text=_('the datetime the transaction was billed'),
#         verbose_name='transaction date',
#     )
#     amount = models.DecimalField(
#         blank=True,
#         decimal_places=4,
#         help_text=_('how much was billed for the user'),
#         max_digits=19,
#         null=True,
#     )
#
#     class Meta:
#         ordering = ('date_transaction', 'employer',)


class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='%(class)s_created')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='%(class)s_modified')
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class emp_subscription(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, verbose_name='ID',)
    employer = models.OneToOneField(employer, on_delete=models.CASCADE)
    plan = models.ForeignKey('subscription_plan', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.id)

    def used_jobs(self):
        return self.employer.jobs.filter(created_at__gte=self.start_date, created_at__lte=self.end_date).count()

    def remaining_jobs(self):
        used_jobs = self.used_jobs()
        return self.plan.jobs - used_jobs

    def used_suggestions(self):
        return self.employer.suggestions.filter(created_at__gte=self.start_date, created_at__lte=self.end_date).count()

    def remaining_suggestions(self):
        used_suggestions = self.used_suggestions()
        return self.plan.suggestions - used_suggestions

    def is_active(self):
        return self.end_date >= timezone.now().date()


class emp_transaction(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, verbose_name='ID',)
    employer = models.ForeignKey(employer, on_delete=models.CASCADE)
    subscription = models.ForeignKey(emp_subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f"Transaction #{self.id} for {self.employer.company}"

# class Plan(BaseModel):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     job_limit = models.PositiveIntegerField()
#     suggestion_limit = models.PositiveIntegerField()
#
#     def __str__(self):
#         return self.name



class job(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    employer = models.ForeignKey(employer, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200, verbose_name=_('Job Title'))
    keywords = TagField(verbose_name=_('Position keywords'),
                        delimiters=' ')
    job_description = RichTextField(default='',
                                    blank=False, null=False, verbose_name=_('Job Description'))
    job_type = models.CharField(max_length=20, choices=Employment_Type,
                                default="Full-time", blank=False, null=False, verbose_name=_('Employment Type'))
    date_opened = models.DateField(
        default=timezone.now, verbose_name=_('Date opened'))
    date_closed = models.DateField(verbose_name=_(
        'Date closed'), blank=True, null=True)
    city = models.CharField(max_length=500, default='Baghdad',
                            choices=GOVERNORATES, verbose_name=_('City'))
    country = CountryField(blank_label=_(
        '(select country)'), default='IQ', verbose_name=_('Country'))
    salary = models.IntegerField(
        verbose_name=_('Salary'), blank=True, null=True)
    nationality = models.CharField(max_length=15, choices=NATIONALITY,
                                   default="both", blank=False, null=False, verbose_name=_('Nationality'))

    applied_candidates = models.ManyToManyField(
        candidate, blank=True, verbose_name=_('Applied Candidates'))
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

    class Meta:
        ordering = ('-date_opened',)
