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
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from datetime import date, timedelta
from django.db.models import F


NATIONALITY = [
    ('international', _('International')),
    ('national', _('National')),
    ('both', _('Both')),
]

PLAN_STATUS = [
    ('Active', _('Active')),
    ('Disabled', _('Disabled')),
    ('ComingSoon', _('Coming Soon')),
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


class subscription_features(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    feature = models.CharField(max_length=200, verbose_name=_('Feature'))

    def __str__(self):
        return self.feature

    def __unicode__(self):
        return self.feature


class subscription_plan(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.CharField(max_length=200, verbose_name=_('plan'))
    suggestions = models.IntegerField(verbose_name=_('suggestions'))
    jobs = models.IntegerField(verbose_name=_('Jobs'))
    price = models.IntegerField(verbose_name=_('Price'))
    days = models.IntegerField()
    features = models.ManyToManyField(blank=True, verbose_name=_(
        'Features'), related_name='features', to=subscription_features)
    status = models.CharField(choices=PLAN_STATUS, default='Disabled', max_length=20, verbose_name='Status')
    is_active = models.BooleanField(
        default=False, verbose_name=_('Is Active'))

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



class job(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    employer = models.ForeignKey(
        'employer', on_delete=models.CASCADE, related_name='jobs')
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


    @property
    def is_active(self):
        today = datetime.today()
        return self.date_closed <= today

class employer(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('User'))
    company = models.CharField(max_length=200, verbose_name=_('Company Name'))
    logo = ThumbnailerImageField(
        upload_to='company_logos', blank=False, null=False,  verbose_name=_('Logo'))
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
        ordering = ('company',)

    def get_current_subscription_info(self):
        today = date.today()
        active_subscriptions = Subscription.objects.filter(
            employer=self,
            end_date__gte=today
        )

        active_jobs = 0
        used_jobs = 0
        start_active_subscriptions = date(year=9999, month=12, day=31)
        end_active_subscriptions = date(year=1900, month=1, day=1)
        for subscription in active_subscriptions:
            active_jobs += subscription.plan.jobs
            if subscription.start_date < start_active_subscriptions:
                start_active_subscriptions = subscription.start_date
            if subscription.end_date > end_active_subscriptions:
                end_active_subscriptions = subscription.end_date
        used_jobs = job.objects.filter(
            created_at__gte=start_active_subscriptions,
            created_at__lte=end_active_subscriptions
        ).count()

        remaining_jobs = active_jobs - used_jobs

        return {
            'active_jobs': active_jobs,
            'remaining_jobs': remaining_jobs,
            'used_jobs': used_jobs,
            'active_subscriptions': active_subscriptions,
            'start_active_subscriptions': start_active_subscriptions,
            'end_active_subscriptions': end_active_subscriptions,
            'active_subscriptions_count': active_subscriptions.count()
        }
class suggestion(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    employer = models.ForeignKey(
        employer, on_delete=models.CASCADE, related_name='suggestions')
    candidate = models.ForeignKey(
        candidate, on_delete=models.CASCADE, related_name='candidates', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True)
    modified_by = models.ForeignKey(
        User, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = ('-created_at',)




class Checkout(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    employer = models.ForeignKey(employer, on_delete=models.CASCADE)
    # subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE)
    plan = models.ForeignKey(
        'subscription_plan', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Plan'))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)
    checkout_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True)
    modified_by = models.ForeignKey(
        User, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Subscription(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    employer = models.ForeignKey(employer, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        'subscription_plan', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Plan'))
    checkout = models.ForeignKey(
        'Checkout', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Checkout'))
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True)
    modified_by = models.ForeignKey(
        User, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.employer.company

    def used_jobs(self):
        # Calculate the count of jobs created within the subscription period
        return self.employer.jobs.filter(created_at__gte=self.start_date, created_at__lte=self.end_date).count()

    def used_suggestions(self):
        # Calculate the count of suggestions created within the subscription period
        return self.employer.suggestions.filter(created_at__gte=self.start_date, created_at__lte=self.end_date).count()

    def remaining_jobs(self):
        return self.plan.jobs - self.used_jobs()

    def remaining_suggestions(self):
        return self.plan.suggestions - self.used_suggestions()

    def is_active(self):
        return self.end_date >= timezone.now().date()

    def is_conflict(self, start_date, end_date):
        selected_start_date = start_date
        selected_end_date = end_date
        current_start_date = self.start_date
        current_end_date = self.end_date
        if (selected_start_date >= current_start_date and selected_start_date <= current_end_date) or (selected_end_date >= current_start_date and selected_end_date <= current_end_date):
            return True
        else:
            return False
