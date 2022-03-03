from audioop import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.core.paginator import Paginator
import json
from candidate.models import candidate
from employer.models import employer, subscription_plan
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
import urllib


def after(request):
    return render(request, 'after_register.html')


def home(request):
    if request.method == 'POST':
        if request.POST.get('keywords'):
            keywords = request.POST.get('keywords')
            request.session['keywords'] = keywords
        if request.POST.get('city'):
            city = request.POST.get('city')
            request.session['city'] = city
        if request.POST.get('education'):
            education = request.POST.get('education')
            request.session['education'] = education
        if request.POST.get('number_of_records'):
            number_of_records = request.POST.get('number_of_records')
            request.session['number_of_records'] = int(number_of_records)
        if request.POST.get('clear'):
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
        context = {
            'keywords': keywords,
            'city': city,
            'education': education,
            'number_of_records': number_of_records,

        }
        return redirect('/candidates/?' + urllib.parse.urlencode(context))
    else:
        employer_details = []
        try:
            userid = request.user.id
            employer_details = employer.objects.get(user__id=userid)
            eid = employer.objects.get(user__id=userid).id
            isemployer = True
        except ObjectDoesNotExist:
            isemployer = False
        context = {
            'princing': subscription_plan.objects.all(),
            'allemployers': employer.objects.filter(public_company_info='Y'),
            'employer_details': employer_details,
            'isemployer': isemployer
        }
        return render(request, 'index.html', context=context)


def about(request):
    return render(request, 'about.html')


def jobdetails(request):
    return render(request, 'job-details.html')


def privacypolicy(request):
    return render(request, 'privacy-policy.html')


def termsconditions(request):
    return render(request, 'terms-conditions.html')
