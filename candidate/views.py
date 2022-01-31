from django.db.models.expressions import Exists
from abc import ABC
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from xhtml2pdf import context
from .models import candidate, education, employment
from accounts.models import User
from vendor.models import vendor
from django.core.paginator import Paginator
import json
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View
from django.urls import reverse_lazy
from .forms import EduForm, EmpForm
from .pdf_process import html_to_pdf
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def candlist(request):
    if request.method == 'GET':
        if request.GET.get('country'):
            country = request.GET.get('country')
            request.session['country'] = country
        if request.GET.get('skills'):
            skills = request.GET.get('skills')
            request.session['skills'] = skills

        if request.GET.get('number_of_records'):
            number_of_records = request.GET.get('number_of_records')
            request.session['number_of_records'] = int(number_of_records)
        if request.GET.get('clear'):
            if request.session.get('country'):
                del request.session['country']
            if request.session.get('skills'):
                del request.session['skills']
            if request.session.get('number_of_records'):
                del request.session['number_of_records']
    country = request.session.get('country')
    skills = request.session.get('skills')
    number_of_records = request.session.get('number_of_records')
    cand_list = candidate.objects.all()
    if number_of_records:
        number_of_records = int(number_of_records)
    else:
        number_of_records = 10
    if country:
        cand_list = cand_list.filter(country__icontains=country)
    if skills:
        cand_list = cand_list.filter(skills__icontains=skills)
    session = [country, skills, number_of_records]
    # Show 25 contacts per page.
    paginator = Paginator(cand_list, number_of_records)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'session': json.dumps(session),
        'page_obj': page_obj,
        'remcand': vendor.objects.filter(user=request.user).order_by().values_list('remaining_records', flat=True).first()
    }
    return render(request, 'candidate/cand_list.html', context)


def candetials(request, cid):
    user = request.user
    cm = {}
    remcand = vendor.objects.get(user=request.user)
    if remcand.remaining_records > 0:
        cm = candidate.objects.get(id=cid)
        remcand.remaining_records = remcand.remaining_records - 1
        remcand.save()
    context = {
        'object': cm,
        'educations': education.objects.filter(candidate__id=cid),
        'employments': employment.objects.filter(candidate__id=cid),
        'remcand': remcand.remaining_records
    }
    return render(request, 'candidate/candidate_detail.html', context)


class EducationCreateView(CreateView):
    model = education
    fields = ['education_level', 'country', 'city', 'institution',
              'original_title_of_the_qualification', 'main_subject', 'start_date', 'graduation_date']

    def form_valid(self, form):
        self.object = form.save()
        candidate.education.add(self.object)


def my_candidate_details(request):

    try:
        userid = request.user.id
        candidate_detials = candidate.objects.get(user__id=userid)
        cid = candidate.objects.get(user__id=userid).id
        context = {
            'object': candidate_detials,
            'educations': education.objects.filter(candidate__id=cid),
            'employments': employment.objects.filter(candidate__id=cid)
        }
        return render(request, 'candidate/my_candidate_details.html', context)
    except ObjectDoesNotExist:
        return redirect('home')


def del_education(request, eid):
    userid = request.user.id
    cid = candidate.objects.get(user__id=userid).id
    msg = ""
    if education.objects.filter(id=eid).exists() and education.objects.filter(candidate__id=cid).exists():
        education.objects.filter(id=eid).delete()
        return JsonResponse({"data": ""}, status=200)
    else:
        return JsonResponse({"data": ""}, status=400)


def del_employement(request, eid):
    userid = request.user.id
    cid = candidate.objects.get(user__id=userid).id
    msg = ""
    if employment.objects.filter(id=eid).exists() and employment.objects.filter(candidate__id=cid).exists():
        employment.objects.filter(id=eid).delete()
        return JsonResponse({"data": ""}, status=200)
    else:
        return JsonResponse({"data": ""}, status=400)


class EducationCreateView(CreateView):
    model = education
    template_name = 'candidate/education/create.html'
    form_class = EduForm

    def form_valid(self, form):
        current_candidate = candidate.objects.get(
            user__id=self.request.user.id)
        Edu = form.save(commit=False)
        Edu.created_by = User.objects.get(email=self.request.user.email)

        Edu.save()
        Edu.candidate_set.add(current_candidate)
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
        return reverse_lazy('my_candidate_details')


class EducationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = education
    template_name = 'candidate/education/create.html'
    fields = ['education_level', 'country', 'city', 'institution',
              'original_title_of_the_qualification', 'main_subject', 'start_date',
              'graduation_date']

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_candidate_details')

    def test_func(self):
        return True


class EmploymentCreateView(CreateView):
    model = employment
    template_name = 'candidate/employment/create.html'
    form_class = EmpForm

    def form_valid(self, form):
        current_candidate = candidate.objects.get(
            user__id=self.request.user.id)
        Emp = form.save(commit=False)
        Emp.created_by = User.objects.get(email=self.request.user.email)

        Emp.save()
        Emp.candidate_set.add(current_candidate)
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
        return reverse_lazy('my_candidate_details')


class EmploymentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = employment
    template_name = 'candidate/employment/create.html'
    fields = ['employer', 'country', 'city', 'current_job',
              'start_date', 'end_date', 'job_title',
              'reason_for_leaving']

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_candidate_details')

    def test_func(self):
        return True


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        userid = request.user.id
        candidate_detials = candidate.objects.get(user__id=userid)
        cid = candidate.objects.get(user__id=userid).id
        context = {
            'object': candidate_detials,
            'educations': education.objects.filter(candidate__id=cid),
            'employments': employment.objects.filter(candidate__id=cid)
        }
        # getting the template
        pdf = html_to_pdf('candidate/cv copy.html', context)

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
