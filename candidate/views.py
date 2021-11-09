from django.shortcuts import render, redirect
from .models import candidate
from vendor.models import vendor
from django.core.paginator import Paginator
import json
# Create your views here.
def candlist(request):
    if request.method == 'GET':
        if request.GET.get('salary_desired'):
            salary_desired = request.GET.get('salary_desired')
            request.session['salary_desired'] = salary_desired
        if request.GET.get('university'):
            university = request.GET.get('university')
            request.session['university'] = university
        if request.GET.get('skills'):
            skills = request.GET.get('skills')
            request.session['skills'] = skills
        if request.GET.get('graduation_year'):
            graduation_year = request.GET.get('graduation_year')
            request.session['graduation_year'] = int(graduation_year)
        if request.GET.get('number_of_records'):
            number_of_records = request.GET.get('number_of_records')
            request.session['number_of_records'] = int(number_of_records)
        if request.GET.get('clear'):
            if request.session.get('salary_desired'):
                del request.session['salary_desired']
            if request.session.get('university'):
                del request.session['university']
            if request.session.get('skills'):
                del request.session['skills']
            if request.session.get('graduation_year'):
                del request.session['graduation_year']
            if request.session.get('number_of_records'):
                del request.session['number_of_records']
    salary_desired = request.session.get('salary_desired')
    university = request.session.get('university')
    skills = request.session.get('skills')
    graduation_year = request.session.get('graduation_year')
    number_of_records = request.session.get('number_of_records')
    cand_list = candidate.objects.all()
    if number_of_records:
        number_of_records = int(number_of_records)
    else:
        number_of_records = 10
    if salary_desired:
        cand_list = cand_list.filter(salary_desired__icontains=salary_desired)
    if university==0:
        pass
    elif university:
        cand_list = cand_list.filter(university__icontains=university)
    if skills:
        cand_list = cand_list.filter(skills__icontains=skills)
    if graduation_year:
        cand_list = cand_list.filter(graduation_year=graduation_year)
    session = [salary_desired, university, skills, graduation_year, number_of_records]
    # Show 25 contacts per page.
    paginator = Paginator(cand_list, number_of_records)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'session': json.dumps(session),
        'page_obj': page_obj,
        'university': candidate.objects.order_by().values_list('university', flat=True).distinct(),
        'graduation_year': candidate.objects.order_by().values_list('graduation_year', flat=True).distinct(),
        'remcand':vendor.objects.filter(user=request.user).order_by().values_list('remaining_records', flat=True).first()
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
        'remcand':remcand.remaining_records
    }
    return render(request, 'candidate/candidate_detail.html', context)
