from functools import reduce
import operator
import re
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from requests import request
from accounts.models import User
from employer.forms import EmpForm, JobForm, SubscriptionForm
from employer.models import job, employer, subscription_plan, Subscription, suggestion
from django.core.exceptions import ObjectDoesNotExist
from candidate.models import candidate
from django.http.response import JsonResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator
import json
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, force_text
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from abc import ABC
from datetime import timedelta
from datetime import datetime
from django.template.loader import render_to_string
# Create your views here.


def send_review_email(Employer, request):
    current_site = get_current_site(request)
    message = 'text version of HTML message'
    email_subject = 'Your Employer account under review'
    email_body = render_to_string('employer/review.html', {
        'Employer': Employer,
        'domain': current_site,
    })

    send_mail(email_subject, message, settings.DEFAULT_FROM_EMAIL, [
              Employer.user.email], fail_silently=True, html_message=email_body)


def send_employer_email(user, cjob, cand, request):
    current_site = get_current_site(request)
    message = 'text version of HTML message'
    email_subject = 'Candidate apply for job'
    email_body = render_to_string('employer/job/apply.html', {
        'domain': current_site,
        'user': user,
        'job': cjob,
        'emp': cjob.employer,
        'cand': cand
    })

    send_mail(email_subject, message, settings.DEFAULT_FROM_EMAIL, [
              cjob.employer.communication_email], fail_silently=True, html_message=email_body)


class EmployerCreateView(CreateView):
    model = employer
    template_name = 'employer/create.html'
    form_class = EmpForm

    def form_valid(self, form):
       # current_candidate = candidate.objects.get(user__id=self.request.user.id)
        Employer = form.save(commit=False)
        Employer.created_by = User.objects.get(email=self.request.user.email)
        Employer.created_at = datetime.now()
        Employer.is_verified = False
        Employer.user = self.request.user
        currentuser = self.request.user
        currentuser.is_employer = True
        currentuser.save()
        Employer.save()
        send_review_email(Employer, request)
        return super().form_valid(form)

    def get_success_url(self):
        # context = {
        #     'is_verified': False
        # }
        return reverse_lazy('my_employer_details')

    def get_context_data(self, **kwargs):
        ctx = super(EmployerCreateView, self).get_context_data(**kwargs)
        currentuser = self.request.user
        employercount = 0
        current_employer = []
        try:
            employercount = employer.objects.filter(
                user__id=self.request.user.id).count()
        except (employer.DoesNotExist):
            employercount = 0

        if employercount >= 1:
            current_employer = employer.objects.get(
                user__id=self.request.user.id)
            currentuser.is_employer = True
            currentuser.save()
        else:
            currentuser.is_employer = False
            currentuser.save()
        ctx['current_employer'] = current_employer
        return ctx


class JobCreateView(CreateView):
    model = job
    template_name = 'employer/job/create.html'
    form_class = JobForm

    def form_valid(self, form):
       # current_candidate = candidate.objects.get(user__id=self.request.user.id)
        Job = form.save(commit=False)
        user = self.request.user
        remaining_jobs = 0
        employer_subscription_last = Subscription.objects.filter(
            employer__user=user).order_by('-end_date').first()
        if employer_subscription_last:
            employer_subscription = Subscription.objects.get(
                id=employer_subscription_last.id)
            remaining_jobs = employer_subscription.remaining_jobs()
        else:
            messages.add_message(self.request, messages.ERROR,
                                 _("You are not subscribed to us, please subscribe to post a job"))
        current_employer = employer.objects.get(user__id=self.request.user.id)

        if current_employer.is_verified == False:
            messages.add_message(self.request, messages.ERROR,
                                 _("Your employer profile under review"))
        if remaining_jobs >= 1:
            Job.employer = current_employer
            Job.created_by = User.objects.get(email=user.email)
            messages.add_message(self.request, messages.SUCCESS,
                                 _("Your job post is successful"))
            Job.save()
        else:
            messages.add_message(self.request, messages.ERROR,
                                 _("job not posted, please check jobs balance"))
        return super(JobCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_employer_details')

    def get_context_data(self, **kwargs):
        ctx = super(JobCreateView, self).get_context_data(**kwargs)
        user = self.request.user
        employer_subscription = None
        current_employer = employer.objects.get(user__id=self.request.user.id)
        employer_subscription_last = Subscription.objects.filter(
            employer__user=user).order_by('-end_date').first()
        if employer_subscription_last:
            employer_subscription = Subscription.objects.get(
                id=employer_subscription_last.id)
            remaining_jobs = employer_subscription.remaining_jobs()
        else:
            messages.add_message(self.request, messages.ERROR,
                                 _("You are not subscribed to us, please subscribe to post a job"))
        ctx['current_employer'] = current_employer
        ctx['employer_subscription'] = employer_subscription

        return ctx


def job_apply(request, jid):
    if request.method == 'GET':
        try:
            current_candidate = candidate.objects.get(user__id=request.user.id)
            current_job = job.objects.get(id=jid)
            current_job.applied_candidates.add(current_candidate)
            current_job.save()
            send_employer_email(request.user, current_job,
                                current_candidate, request)
            messages.add_message(request, messages.SUCCESS,
                                 _("Your application is successful"))
            return redirect(reverse('job_details', kwargs={"jid": current_job.id}))
        except:
            messages.add_message(request, messages.ERROR,
                                 _("Your application is error"))
            return redirect(reverse('job_details', kwargs={"jid": current_job.id}))


def JobDetails(request, jid):
    user = request.user
    job_details = job.objects.get(id=jid)
    job_closed = False
    current_candidate_applied = False
    is_job_owner = False
    if request.user.is_authenticated:
        if user.is_superuser:
            True
        if user.is_candidate == True:
            current_candidate = candidate.objects.get(user__id=request.user.id)
            is_job_owner = False
            if job.objects.filter(id=jid, applied_candidates=current_candidate).count() >= 1:
                current_candidate_applied = True
            else:
                current_candidate_applied = False

        if user.is_employer == True:
            jeid = job_details.employer.id
            ceid = employer.objects.get(user__id=user.id).id
            if ceid == jeid:
                is_job_owner = True
    if job_details.date_closed is not None:
        job_closed = False if job_details.date_closed >= datetime.today().date() else True
    employer_details = employer.objects.get(jobs__id=job_details.id)
    candidates_list = job_details.applied_candidates.all()
    context = {
        'job': job_details,
        'job_closed': job_closed,
        'now': datetime.now(),
        'applied': current_candidate_applied,
        'employer': employer_details,
        'candidates_list': candidates_list,
        'is_job_owner': is_job_owner
    }
    return render(request, 'employer/job/details.html', context)


def my_employer_details(request):
    userid = request.user.id
    try:

        employer_details = employer.objects.get(user__id=userid)
        eid = employer.objects.get(user__id=userid).id
        employer_subscriptions = Subscription.objects.filter(
            employer_id=eid).order_by('created_at')
        paginator = Paginator(employer_subscriptions, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        page_range = paginator.get_elided_page_range(
            number=page_number, on_each_side=2, on_ends=2)
        suggestions = suggestion.objects.filter(
            employer_id=eid).order_by('-created_at')
        if employer_details.is_verified == False:
            messages.add_message(request, messages.ERROR, _(
                "Your employer profile under review"))
        context = {
            'object': employer_details,
            'suggestions': suggestions,
            'jobs': job.objects.filter(employer__id=eid),
            'page_obj': page_obj,
            'page_range': page_range,
        }
        return render(request, 'employer/my_employer_details.html', context)
    except ObjectDoesNotExist:
        context = {
            'isemployer': 'false'
        }
        return render(request, 'employer/my_employer_details.html', context)


def employer_details(request, eid):

    try:
        userid = request.user.id
        employer_details = employer.objects.get(id=eid)
        context = {
            'object': employer_details,
            'jobs': job.objects.filter(employer__id=eid),
        }
        return render(request, 'employer/employer_details.html', context)
    except ObjectDoesNotExist:
        context = {
            'isemployer': 'false'
        }
        return render(request, 'employer/employer_details.html', context)


def job_list(request):
    if request.method == 'GET':
        if request.GET.get('city'):
            city = request.GET.get('city')
            request.session['city'] = city
        else:
            city = ""
            request.session['city'] = city
        if request.GET.get('keywords'):
            keywords = request.GET.get('keywords')
            request.session['keywords'] = keywords
        else:
            keywords = ""
            request.session['keywords'] = keywords
        if request.GET.get('number_of_records'):
            number_of_records = request.GET.get('number_of_records')
            try:
                request.session['number_of_records'] = int(number_of_records)
            except:
                request.session['number_of_records'] = 50
        if request.GET.get('clear'):
            if request.session.get('city'):
                del request.session['city']
            if request.session.get('keywords'):
                del request.session['keywords']
            if request.session.get('number_of_records'):
                del request.session['number_of_records']
    city = request.session.get('city')
    keywords = request.session.get('keywords')
    number_of_records = request.session.get('number_of_records')
    job_list3 = job.objects.all()
    job_list = job.objects.all()
    job_list1 = []
    if number_of_records:
        number_of_records = int(number_of_records)
    else:
        number_of_records = 50
    if city:
        job_list = job_list.filter(city=city)
    if keywords:
        query_words = str(keywords).split(" ")  # Get the word in a list
        query = Q()
        for w in query_words:
            if len(w) < 2:  # Min length
                query_words.remove(w)
        for word in query_words:
            query = query | Q(job_title__icontains=word) | Q(
                employer__company__icontains=word) | Q(keywords__icontains=word)

        job_list1 = job_list.filter(query)
        # job_list1.union(job_list1)
        # job_list2 = job_list.filter(reduce(lambda x, y: x | y, [Q(employer__company__icontains=word)
        #                                                         for word in query_words]))
        # # job_list1.union(job_list2)
        # job_list3 = job_list.filter(reduce(lambda x, y: x | y, [Q(keywords__icontains=word)
        #                                                         for word in query_words]))
        # job_list1.union(job_list1, job_list2, job_list3)
    else:
        job_list1 = job_list3.order_by('-date_opened')
    session = [keywords, city, number_of_records]
    # Show 25 contacts per page.
    paginator = Paginator(job_list1, number_of_records)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(
        number=page_number, on_each_side=2, on_ends=2)
    context = {
        'session': json.dumps(session),
        'page_obj': page_obj,
        'page_range': page_range,
        'jobs_count': job_list1.count(),
    }
    return render(request, 'employer/job/job_list.html', context)


class EmployerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = employer
    template_name = 'employer/update.html'
    form_class = EmpForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_employer_details')

    def test_func(self):
        return True


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = job
    template_name = 'employer/job/update.html'
    form_class = JobForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('job_details', kwargs={"jid": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currentuser = self.request.user
        if currentuser.is_employer == True:
            context['is_employer'] = True
            current_employer = employer.objects.get(
                user__id=self.request.user.id)
            current_job = job.objects.get(id=self.object.id)
            if current_job.employer == current_employer:
                context['ownjob'] = True
            else:
                context['ownjob'] = False
        else:
            context['is_employer'] = False
        context['id'] = self.object.id
        return context

    def test_func(self):
        return True


# class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
#     model = job
#     template_name = 'employer/job/update.html'
#     form_class = JobForm

#     def form_valid(self, form):
#         return super().form_valid(form)

#     def get_success_url(self, **kwargs):
#         return redirect(reverse('job_details', args=(self.object.id,)))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['id'] = self.object.id
#         return context

#     def test_func(self):
#         return True


def employer_plan(request, sid):
    if request.user.is_employer:
        try:
            current_employer = employer.objects.get(user__id=request.user.id)
        except (employer.DoesNotExist):
            return JsonResponse({"data": "You employer not found, please try agin later"}, status=200)
        employer_subscriptions = Subscription.objects.filter(
            employer__user=request.user).order_by('-created_at')
        if employer_subscriptions.count() > 0 and employer_subscriptions.first().is_active():
            return JsonResponse({"data": f"You already subscribed with us with plan {employer_subscriptions.first().plan} end at {employer_subscriptions.first().end_date}"}, status=200)
        else:
            plan = subscription_plan.objects.get(id=sid)
            emp_subscription = Subscription(employer=current_employer, plan=plan, start_date=datetime.now(
            ), end_date=datetime.now() + timedelta(plan.days), created_at=datetime.now(), created_by=request.user)
            emp_subscription.save()
            return JsonResponse({"data": "subscription successfully"}, status=200)


def send_verified(request, employerid):
    selected_employer = employer.objects.get(id=employerid)
    selected_employer.is_verified = True
    selected_employer.save()
    message = 'text version of HTML message'
    email_subject = 'Your Employer Profile Verified'
    email_body = render_to_string('employer/verified.html', {
        'employer': selected_employer,
        'uid': urlsafe_base64_encode(force_bytes(selected_employer.pk)),
    })

    send_mail(email_subject, message, settings.DEFAULT_FROM_EMAIL, [
              selected_employer.user.email], fail_silently=True, html_message=email_body)
    return redirect('dashboard')


class SubscriptionCreateView(CreateView):
    model = Subscription
    template_name = 'employer/subscription/create.html'
    form_class = SubscriptionForm
    success_message = 'Success: Subscription was created.'
    success_url = reverse_lazy('subscriptions_list')

    def form_valid(self, form):
        # current_candidate = candidate.objects.get(
        #     user__id=self.request.user.id)
        subscription = form.save(commit=False)
        subscription.end_date = subscription.start_date + \
            timedelta(days=subscription.plan.days)
        employer_subscriptions = Subscription.objects.filter(Q(employer=subscription.employer), Q(
            start_date__lte=subscription.end_date), Q(end_date__gte=subscription.start_date))
        if employer_subscriptions.count() >= 1:
            form.add_error(
                'employer', 'The chosen employer is already subscribed in the same period.')
            return super().form_invalid(form)
        subscription.created_by = User.objects.get(
            email=self.request.user.email)
        subscription.created_at = datetime.now()
        subscription.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('subscriptions_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employer_subscriptions = {}
        subscription = self.request.POST if self.request.method == 'POST' else None
        employer_plan = subscription_plan.objects.get(
            id=subscription.get('plan')) if subscription else None
        subscription_employer = subscription.get(
            'employer') if subscription else None
        subscription_start_date_str = subscription.get(
            'start_date') if subscription else None
        subscription_start_date = datetime.strptime(
            subscription_start_date_str, '%Y-%m-%d').date() if subscription_start_date_str else None
        subscription_end_date = subscription_start_date + \
            timedelta(days=employer_plan.days) if subscription else None
        if subscription:
            employer_subscriptions = Subscription.objects.filter(Q(employer_id=subscription_employer), Q(
                start_date__lte=subscription_end_date), Q(end_date__gte=subscription_start_date))
        additional_context = {
            'subscriptions': employer_subscriptions,
        }

        context.update(additional_context)
        return context


class SubscriptionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = Subscription
    template_name = 'employer/subscription/update.html'
    fields = ['employer', 'plan', 'start_date']

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('subscriptions_list')

    def test_func(self):
        return True
