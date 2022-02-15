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
# Create your views here.


class EmployerCreateView(CreateView):
    model = employer
    template_name = 'employer/create.html'
    form_class = EmpForm

    def form_valid(self, form):
       # current_candidate = candidate.objects.get(user__id=self.request.user.id)
        Employer = form.save(commit=False)
        Employer.created_by = User.objects.get(email=self.request.user.email)
        Employer.user = self.request.user
        currentuser = User.objects.filter(id=self.request.user.id)
        currentuser.is_employer = True
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
        userid = self.request.user.id
        employer = employer.objects.get(user__id=userid)
        Job.employer = employer
        Job.created_by = User.objects.get(email=self.request.user.email)
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
            messages.add_message(request, messages.SUCCESS,
                                 _("Your are appiled to job"))
            return redirect(reverse('job_details', kwargs={"jid": current_job.id}))
        except:
            messages.add_message(request, messages.ERROR,
                                 _("There are error on appiled job"))
            return redirect(reverse('job_details', kwargs={"jid": current_job.id}))


def JobDetails(request, jid):
    user = request.user
    job_details = job.objects.get(id=jid)
    current_candidate = candidate.objects.get(user__id=request.user.id)
    if job.objects.filter(id=jid, applied_candidates=current_candidate).count() >= 1:
        current_candidate_applied = True
    else:
        current_candidate_applied = False
    employer_details = employer.objects.get(job__id=job_details.id)
    context = {
        'job': job_details,
        'applied': current_candidate_applied,
        'employer': employer_details
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
        if request.GET.get('country'):
            country = request.GET.get('country')
            request.session['country'] = country
        else:
            country = ""
            request.session['country'] = country
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
            if request.session.get('country'):
                del request.session['country']
            if request.session.get('search'):
                del request.session['keywords']
            if request.session.get('number_of_records'):
                del request.session['number_of_records']
    country = request.session.get('country')
    keywords = request.session.get('keywords')
    number_of_records = request.session.get('number_of_records')
    job_list2 = job.objects.all()
    job_list = job.objects.all()
    if number_of_records:
        number_of_records = int(number_of_records)
    else:
        number_of_records = 10
    if country:
        job_list = job_list.filter(country__icontains=country)
    if keywords:
        query_words = str(keywords).split(" ")  # Get the word in a list
        for w in query_words:
            if len(w) < 2:  # Min length
                query_words.remove(w)

        job_list1 = job_list.filter(reduce(lambda x, y: x | y, [Q(job_title__icontains=word)
                                                                for word in query_words]))
        job_list2 = job_list.filter(reduce(lambda x, y: x | y, [Q(employer__company__icontains=word)
                                                                for word in query_words]))
        job_list2.union(job_list1)
    session = [country, keywords, number_of_records]
    # Show 25 contacts per page.
    paginator = Paginator(job_list2, number_of_records)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'session': json.dumps(session),
        'page_obj': page_obj
    }
    return render(request, 'employer/job/job_list.html', context)
