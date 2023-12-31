from mimetypes import init
from urllib import request
from django.conf import settings
from django.db.models.expressions import Exists
from abc import ABC
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import tempfile
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# from xhtml2pdf import context
from .models import candidate, education, employment, language, certificate
from accounts.models import User
from employer.models import employer, Subscription, suggestion
from django.core.paginator import Paginator
import json
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.views.generic import View
from django.urls import reverse_lazy
from .forms import EduForm, EmpForm, CanForm, LangForm, CerForm
# from .pdf_process import html_to_pdf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from employer.models import job
from bootstrap_modal_forms.generic import BSModalCreateView
from django.db.models import Q
# Create your views here.


def candlist(request):
    if request.method == 'GET':
        if request.GET.get('keywords'):
            keywords = request.GET.get('keywords')
            request.session['keywords'] = keywords
        if request.GET.get('city'):
            city = request.GET.get('city')
            request.session['city'] = city
        if request.GET.get('education'):
            education = request.GET.get('education')
            request.session['education'] = education
        if request.GET.get('number_of_records'):
            number_of_records = request.GET.get('number_of_records')
            try:
                request.session['number_of_records'] = int(number_of_records)
            except:
                request.session['number_of_records'] = 10
        if request.GET.get('clear'):
            if request.session.get('keywords'):
                del request.session['keywords']
            if request.session.get('city'):
                del request.session['city']
            if request.session.get('education'):
                del request.session['education']
            if request.session.get('number_of_records'):
                del request.session['number_of_records']
    keywords = request.session.get('keywords')
    city = request.session.get('city')
    education = request.session.get('education')
    number_of_records = request.session.get('number_of_records')
    cand_list = candidate.objects.all()
    cand_list3 = candidate.objects.all()
    cand_list1 = []
    if number_of_records:
        number_of_records = int(number_of_records)
    else:
        number_of_records = 10
    if city and city != 'All':
        cand_list = cand_list.filter(city=city)
    if education and education != '0':
        cand_list = cand_list.filter(
            highest_level_of_education__icontains=education)
    if keywords:
        query_words = str(keywords).split(" ")  # Get the word in a list
        query = Q()
        for w in query_words:
            if len(w) < 2:  # Min length
                query_words.remove(w)
        for word in query_words:
            query = query | Q(certificate__organization__icontains=word) | Q(
                Employment__job_title__icontains=word) | Q(skills__icontains=word)

        cand_list1 = cand_list.filter(query)
    else:
        cand_list1 = cand_list3
    session = [city, education, number_of_records, keywords]
    # Show 25 contacts per page.
    paginator = Paginator(cand_list1.distinct(), number_of_records)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(number=page_number,on_each_side=2, on_ends=2)
    context = {
        'session': json.dumps(session),
        'page_obj': page_obj,
        'cn': cand_list1,
        'page_range':page_range,
        'candidate_count': cand_list1.count(),
        'remcand': employer.objects.filter(user=request.user).order_by().values_list('remaining_records', flat=True).first()
    }
    return render(request, 'candidate/cand_list.html', context)


def candetials(request, cid):
    cm = candidate.objects.get(id=cid)
    if request.user.is_superuser:
        context = {
            'object': cm,
            'educations': education.objects.filter(candidate__id=cid),
            'employments': employment.objects.filter(candidate__id=cid),
            'Languages': language.objects.filter(candidate__id=cid),
            'certificates': certificate.objects.filter(candidate__id=cid),
        }
    else:
        try:
            remcand = employer.objects.get(user=request.user)
            subscriptions = Subscription.objects.filter(employer=remcand)
            old_suggestions = suggestion.objects.filter(employer=remcand, candidate=cm).count()
            total_subscription = subscriptions.count()
            print('total_subscription: ', total_subscription)
            print('old_suggestions: ', old_suggestions)
        except ObjectDoesNotExist:
            context = {
                'isemployer': 'false'
            }
            return render(request, 'employer/employer_details.html', context)

        if total_subscription > 0:
            
            if remcand.remaining_suggestions() > 0:
                if old_suggestions == 0:
                    new_suggestion = suggestion.objects.create(employer=remcand, candidate=cm)

                    new_suggestion.save()
                    print(new_suggestion.id)
                context = {
                    'object': cm,
                    'educations': education.objects.filter(candidate__id=cid),
                    'employments': employment.objects.filter(candidate__id=cid),
                    'Languages': language.objects.filter(candidate__id=cid),
                    'certificates': certificate.objects.filter(candidate__id=cid),
                    'remcand': remcand.remaining_records
                }
            else:
                context = {
                    'msg': "You don't have more balance for suggestions"
                }
        else:
            context = {
                    'msg': "Please subscribe with us to view candidate details"
                }
    return render(request, 'candidate/candidate_detail.html', context)


class CandidateDetail(DetailView):
    model = candidate
    template_name = 'candidate/my_candidate_details.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        userid = self.request.user.id
        candidate_detials = candidate.objects.get(user__id=userid)
        cid = candidate.objects.get(user__id=userid).id
        context['object'] = candidate_detials
        context['educations'] = education.objects.filter(candidate__id=cid)
        context['employments'] = employment.objects.filter(candidate__id=cid)
        context['Languages'] = language.objects.filter(candidate__id=cid)
        context['certificates'] = certificate.objects.filter(candidate__id=cid)
        return context


def my_candidate_details(request):

    try:
        userid = request.user.id
        candidate_detials = candidate.objects.get(user__id=userid)
        cid = candidate.objects.get(user__id=userid).id
        context = {
            'object': candidate_detials,
            'educations': education.objects.filter(candidate__id=cid),
            'employments': employment.objects.filter(candidate__id=cid),
            'Languages': language.objects.filter(candidate__id=cid),
            'certificates': certificate.objects.filter(candidate__id=cid),
            'applied_jobs': job.objects.filter(applied_candidates=candidate_detials)
        }
        return render(request, 'candidate/my_candidate_details.html', context)
    except ObjectDoesNotExist:
        context = {
            'iscandidate': 'false'
        }
        return render(request, 'candidate/my_candidate_details.html', context)


def del_education(request, eid):
    userid = request.user.id
    cid = candidate.objects.get(user__id=userid).id
    msg = ""
    if education.objects.filter(id=eid).exists() and education.objects.filter(candidate__id=cid).exists():
        education.objects.filter(id=eid).delete()
        return JsonResponse({"data": ""}, status=200)
    else:
        return JsonResponse({"data": ""}, status=400)


def del_certificate(request, eid):
    userid = request.user.id
    cid = candidate.objects.get(user__id=userid).id
    msg = ""
    if certificate.objects.filter(id=eid).exists() and certificate.objects.filter(candidate__id=cid).exists():
        certificate.objects.filter(id=eid).delete()
        return JsonResponse({"data": ""}, status=200)
    else:
        return JsonResponse({"data": ""}, status=400)


def del_employement(request, eid):
    if request.method == 'GET':
        userid = request.user.id
        cid = candidate.objects.get(user__id=userid).id
        msg = ""
        if employment.objects.filter(id=eid).exists() and employment.objects.filter(candidate__id=cid).exists():
            employment.objects.filter(id=eid).delete()
            return JsonResponse({"data": ""}, status=200)
        else:
            return JsonResponse({"data": ""}, status=400)
    else:
        return JsonResponse({"data": ""}, status=405)


def del_language(request, eid):
    if request.method == 'GET':
        userid = request.user.id
        cid = candidate.objects.get(user__id=userid).id
        msg = ""
        if language.objects.filter(id=eid).exists() and language.objects.filter(candidate__id=cid).exists():
            language.objects.filter(id=eid).delete()
            return JsonResponse({"data": ""}, status=200)
        else:
            return JsonResponse({"data": ""}, status=400)
    else:
        return JsonResponse({"data": ""}, status=405)


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
        if 'save' in self.request.POST:
            return reverse_lazy('my_candidate_details')
        if 'save_new' in self.request.POST:
            return reverse_lazy('educationcreate')


class EducationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = education
    template_name = 'candidate/education/update.html'
    fields = ['education_level', 'country', 'city', 'institution',
              'original_title_of_the_qualification', 'main_subject', 'start_date',
              'graduation_date']

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_candidate_details')

    def test_func(self):
        return True


class CandidateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = candidate
    template_name = 'candidate/update.html'
    form_class = CanForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_candidate_details')

    def test_func(self):
        return True


class CertificateCreateView(CreateView):
    model = certificate
    template_name = 'candidate/certificate/create.html'
    form_class = CerForm

    def form_valid(self, form):
        current_candidate = candidate.objects.get(
            user__id=self.request.user.id)
        Cer = form.save(commit=False)
        Cer.created_by = User.objects.get(email=self.request.user.email)

        Cer.save()
        Cer.candidate_set.add(current_candidate)
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
        if 'save' in self.request.POST:
            return reverse_lazy('my_candidate_details')
        if 'save_new' in self.request.POST:
            return reverse_lazy('certificatecreate')


class CertificateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = certificate
    template_name = 'candidate/certificate/update.html'
    fields = ['certificate_name', 'organization',
              'issue_date', 'expire_date', 'expired_certificate', 'attach']

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_candidate_details')

    def test_func(self):
        return True


class LanguageCreateView(CreateView):
    model = language
    template_name = 'candidate/language/create.html'
    form_class = LangForm
    # success_message = 'Success: Book was created.'
    # success_url = reverse_lazy('my_candidate_details')

    def form_valid(self, form):
        current_candidate = candidate.objects.get(
            user__id=self.request.user.id)
        Lang = form.save(commit=False)
        Lang.created_by = User.objects.get(email=self.request.user.email)

        Lang.save()
        Lang.candidate_set.add(current_candidate)
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
        if 'save' in self.request.POST:
            return reverse_lazy('my_candidate_details')
        if 'save_new' in self.request.POST:
            return reverse_lazy('languagecreate')


class LanguageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = language
    template_name = 'candidate/language/update.html'
    fields = ['language', 'level']

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
        if 'save' in self.request.POST:
            return reverse_lazy('my_candidate_details')
        if 'save_new' in self.request.POST:
            return reverse_lazy('employmentcreate')


class CandidateCreateView(CreateView):
    model = candidate
    template_name = 'candidate/create.html'
    form_class = CanForm
    error_meesage = "Error saving the Candidate, check fields below."

    def form_valid(self, form):
        try:
            mycand = candidate.objects.get(user=self.request.user)
            messages.add_message(self.request, messages.ERROR,
                                 "Error saving the Candidate, You registered as below candidate")
        except candidate.DoesNotExist:
            Candidate = form.save(commit=False)
            Candidate.created_by = User.objects.get(
                email=self.request.user.email)
            Candidate.user = self.request.user
            currentuser = self.request.user
            currentuser.is_candidate = True
            currentuser.save()
            Candidate.save()
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
    template_name = 'candidate/employment/update.html'
    fields = ['employer', 'employer_industry', 'country', 'city', 'current_job',
              'start_date', 'end_date', 'job_title', 'supervisor_name', 'supervisor_title', 'supervisor_phone', 'supervisor_email',
              'reason_for_leaving']

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_candidate_details')

    def test_func(self):
        return True


def pdf(request):
    return render(request, 'candidate/resume.html')


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        userid = request.user.id
        candidate_detials = candidate.objects.get(user__id=userid)
        cid = candidate.objects.get(user__id=userid).id
        context = {
            'object': candidate_detials,
            'educations': education.objects.filter(candidate__id=cid),
            # 'employments': employment.objects.filter(candidate__id=cid)
        }
        # getting the template
        pdf = html_to_pdf('candidate/resume.html', context)

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


def generate_pdf(request):
    userid = request.user.id
    try:
        candidate_detials = candidate.objects.get(user__id=userid)
        cid = candidate.objects.get(user__id=userid).id
    except ObjectDoesNotExist:
        return reverse_lazy('my_candidate_details')
    context = {
        'object': candidate_detials,
        'educations': education.objects.filter(candidate__id=cid),
        'employments': employment.objects.filter(candidate__id=cid),
        'Languages': language.objects.filter(candidate__id=cid),
        'certificates': certificate.objects.filter(candidate__id=cid),
    }
    # Rendered
    html_string = render_to_string('candidate/pdf.html', context=context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf(stylesheets=[CSS(string='@page { size: A4; margin: 2cm };'
                                             '* { float: none !important; };'
                                             '@media print { nav { display: none; } }'),
                            settings.BASE_DIR + '/static/css/bootstrap.min.css', ])

    # Creating http response
    # response = HttpResponse(content_type='application/pdf;')
    # response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    # response['Content-Transfer-Encoding'] = 'binary'
    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()
    #     output = open(output.name, 'r')
    #     response.write(output.read())

    return HttpResponse(result, content_type='application/pdf')


def view_pdf(request):
    userid = request.user.id
    try:
        candidate_detials = candidate.objects.get(user__id=userid)
        cid = candidate.objects.get(user__id=userid).id
    except ObjectDoesNotExist:
        return reverse_lazy('my_candidate_details')
    context = {
        'object': candidate_detials,
        'educations': education.objects.filter(candidate__id=cid),
        'employments': employment.objects.filter(candidate__id=cid),
        'Languages': language.objects.filter(candidate__id=cid),
        'certificates': certificate.objects.filter(candidate__id=cid),
    }
    # Rendered
    return render(request, 'candidate/pdf.html', context=context)
