from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from accounts.models import User
from vendor.forms import EmpForm, JobForm
from vendor.models import job, vendor
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


class EmployerCreateView(CreateView):
    model = vendor
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


def my_employer_details(request):

    try:
        userid = request.user.id
        employer_details = vendor.objects.get(user__id=userid)
        eid = vendor.objects.get(user__id=userid).id
        context = {
            'object': employer_details,
            'jobs': job.objects.filter(vendor__id=eid),
        }
        return render(request, 'employer/my_employer_details.html', context)
    except ObjectDoesNotExist:
        context = {
            'isemployer': 'false'
        }
        return render(request, 'employer/my_employer_details.html', context)
