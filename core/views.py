from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.core.paginator import Paginator
import json
from candidate.models import candidate
from employer.models import employer
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    if request.method == 'POST':
        if request.POST.get('country'):
            country = request.POST.get('country')
            request.session['country'] = country
        if request.POST.get('education'):
            education = request.POST.get('education')
            request.session['education'] = education

        if request.POST.get('number_of_records'):
            number_of_records = request.POST.get('number_of_records')
            request.session['number_of_records'] = int(number_of_records)
        if request.POST.get('clear'):
            if request.session.get('country'):
                del request.session['country']
            if request.session.get('education'):
                del request.session['education']
            if request.session.get('number_of_records'):
                del request.session['number_of_records']
        country = request.session.get('country')
        education = request.session.get('education')
        number_of_records = request.session.get('number_of_records')

        session = [country, education, number_of_records]
        return redirect('candlist')
    else:
        return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def jobdetails(request):
    return render(request, 'job-details.html')


def privacypolicy(request):
    return render(request, 'privacy-policy.html')


def termsconditions(request):
    return render(request, 'terms-conditions.html')
