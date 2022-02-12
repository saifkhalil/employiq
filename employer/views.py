from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from accounts.models import User
from employer.forms import EmpForm, JobForm
from employer.models import job, employer
from django.core.exceptions import ObjectDoesNotExist
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


def JobDetails(request, jid):
    user = request.user
    job_details = job.objects.get(id=jid)
    employer = employer.objects.get(job__id=job_details.id)
    context = {
        'job': job_details,
        'employer': employer
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
