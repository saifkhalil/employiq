from functools import reduce
import operator
import re
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from accounts.models import User
from employer.forms import EmpForm, JobForm
from employer.models import job, employer
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
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from abc import ABC
# Create your views here.


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
        Employer.user = self.request.user
        currentuser = self.request.user
        currentuser.is_employer = True
        currentuser.save()
        # currentuser.save()
        Employer.save()
        '''
        html_message = render_to_string('mail_template.html', {'cm': Edu})
        send_mail(
            subject='New Change Management Created Reason: ' +
            form.cleaned_data['reason'],
            html_message=html_message,
            message='',
            from_email='isms@qi.iq',
            recipient_list=['saif.ibrahim@qi.iq', 'saif780@gmail.com'],
            fail_silently=False,
        )
        '''
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_employer_details')


class JobCreateView(CreateView):
    model = job
    template_name = 'employer/job/create.html'
    form_class = JobForm

    def form_valid(self, form):
       # current_candidate = candidate.objects.get(user__id=self.request.user.id)
        Job = form.save(commit=False)
        user = self.request.user
        current_employer = employer.objects.get(user__id=user.id)
        Job.employer = current_employer
        Job.created_by = User.objects.get(email=user.email)
        Job.save()
        '''
        html_message = render_to_string('mail_template.html', {'cm': Edu})
        send_mail(
            subject='New Change Management Created Reason: ' +
            form.cleaned_data['reason'],
            html_message=html_message,
            message='',
            from_email='isms@qi.iq',
            recipient_list=['saif.ibrahim@qi.iq', 'saif780@gmail.com'],
            fail_silently=False,
        )
        '''
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_employer_details')


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
    current_candidate = candidate.objects.get(user__id=request.user.id)
    is_job_owner = False
    if job.objects.filter(id=jid, applied_candidates=current_candidate).count() >= 1:
        current_candidate_applied = True
    else:
        current_candidate_applied = False
    try:
        ceid = employer.objects.get(user__id=user.id).id
    except ObjectDoesNotExist:
        cied = []
    jeid = job_details.employer.id
    if ceid == jeid:
        is_job_owner = True
    employer_details = employer.objects.get(job__id=job_details.id)
    candidates_list = job_details.applied_candidates.all()
    context = {
        'job': job_details,
        'applied': current_candidate_applied,
        'employer': employer_details,
        'candidates_list': candidates_list,
        'is_job_owner': is_job_owner
    }
    return render(request, 'employer/job/details.html', context)


def my_employer_details(request):

    try:
        userid = request.user.id
        employer_details = employer.objects.get(user__id=userid)
        eid = employer.objects.get(user__id=userid).id
        context = {
            'object': employer_details,
            'jobs': job.objects.filter(employer__id=eid),
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
            request.session['number_of_records'] = int(number_of_records)
        if request.GET.get('clear'):
            if request.session.get('city'):
                del request.session['city']
            if request.session.get('search'):
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
        number_of_records = 10
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
        job_list1 = job_list3
    session = [keywords, city, number_of_records]
    # Show 25 contacts per page.
    paginator = Paginator(job_list1, number_of_records)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'session': json.dumps(session),
        'page_obj': page_obj
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
