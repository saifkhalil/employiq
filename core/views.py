from audioop import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.core.paginator import Paginator
import json
from candidate.models import candidate
from employer.models import Subscription, employer, subscription_plan
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
import urllib
from employer.models import employer, job
from accounts.models import User
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
import geoip2.database
from django.db.models import Q


def get_client_ip(request):
    """  Getting client Ip  """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def after(request):
    return render(request, 'after_register.html')


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    active_users_count = User.objects.filter(is_verified=True).count()
    candidates_count = candidate.objects.all().count()
    employers_count = employer.objects.all().count()
    jobs_count = job.objects.all().count()
    users = User.objects.all()
    employers = employer.objects.all().order_by('-created_at')
    candidates = candidate.objects.all()
    users_count = User.objects.all().count()
    context = {
        'active_users_count': active_users_count,
        'candidates_count': candidates_count,
        'employers_count': employers_count,
        'jobs_count': jobs_count,
        'users': users,
        'employers': employers,
        'candidates': candidates,
        'users_count': users_count,
    }
    return render(request, 'dashboard.html', context=context)


def users_list(request):
    users_list = User.objects.all()
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(
        number=page_number, on_each_side=2, on_ends=2)
    context = {
        'page_obj': page_obj,
        'page_range': page_range,
    }
    return render(request, 'dashboard/users.html', context)


def employers_list(request):
    employers_list = {}
    employers = employer.objects.all()
    if request.method == 'GET':
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
                request.session['number_of_records'] = 10
        else:
            number_of_records = 10
        if request.GET.get('clear'):
            if request.session.get('keywords'):
                del request.session['keywords']
            if request.session.get('number_of_records'):
                del request.session['number_of_records']
    keywords = request.session.get('keywords')
    if keywords:
        query_words = str(keywords).split(" ")  # Get the word in a list
        query = Q()
        for w in query_words:
            if len(w) < 2:  # Min length
                query_words.remove(w)
        for word in query_words:
            query = query | Q(company__icontains=word) | Q(
                user__email__icontains=word)
        employers_list = employers.filter(query).order_by('-created_at')
    else:
        employers_list = employers.order_by('-created_at')
    session = [keywords, number_of_records]
    paginator = Paginator(employers_list, number_of_records)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(
        number=page_number, on_each_side=2, on_ends=2)
    context = {
        'session': json.dumps(session),
        'page_obj': page_obj,
        'page_range': page_range,
    }
    return render(request, 'dashboard/employers.html', context)


def candidates_list(request):
    candidates_list = {}
    candidates = candidate.objects.all()
    if request.method == 'GET':
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
                request.session['number_of_records'] = 10
        else:
            number_of_records = 10
        if request.GET.get('clear'):
            if request.session.get('keywords'):
                del request.session['keywords']
            if request.session.get('number_of_records'):
                del request.session['number_of_records']
    keywords = request.session.get('keywords')
    if keywords:
        query_words = str(keywords).split(" ")  # Get the word in a list
        query = Q()
        for w in query_words:
            if len(w) < 2:  # Min length
                query_words.remove(w)
        for word in query_words:
            query = query | Q(firstname__icontains=word) | Q(secondname__icontains=word) | Q(
                lastname__icontains=word) | Q(email__icontains=word) | Q(phone_number__icontains=word)

        candidates_list = candidates.filter(query).order_by('-created_at')
    else:
        candidates_list = candidates.order_by('-created_at')
    session = [keywords, number_of_records]
    paginator = Paginator(candidates_list, number_of_records)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(
        number=page_number, on_each_side=2, on_ends=2)
    context = {
        'session': json.dumps(session),
        'page_obj': page_obj,
        'page_range': page_range,
    }
    return render(request, 'dashboard/candidates.html', context)


# def candidates_list(request):
#     candidates_list = candidate.objects.all()
#     paginator = Paginator(candidates_list, 10)
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)
#     page_range = paginator.get_elided_page_range(
#         number=page_number, on_each_side=2, on_ends=2)
#     context = {
#         'page_obj': page_obj,
#         'page_range': page_range,
#     }
#     return render(request, 'dashboard/candidates.html', context)


def subscriptions_list(request):
    subscriptions_list = Subscription.objects.all()
    paginator = Paginator(subscriptions_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(
        number=page_number, on_each_side=2, on_ends=2)
    context = {
        'page_obj': page_obj,
        'page_range': page_range,
    }
    return render(request, 'dashboard/subscriptions.html', context)


def home(request):
    ip_adresse = get_client_ip(request)
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
            'ip_adresse': ip_adresse,

        }
        return redirect('/candidates/?' + urllib.parse.urlencode(context))
    else:
        employer_details = []
        users = User.objects.all()
        employers = employer.objects.all()
        candidates = candidate.objects.all()
        active_users_count = User.objects.filter(is_verified=True).count()
        candidates_count = candidates.count()
        newest_employers = employers.order_by('-created_at')[:20]
        employers_count = employers.count()
        jobs_count = job.objects.all().count()
        users_count = users.count()
        # plan_dict = dict()
        # plans = subscription_plan.objects.all().order_by('price')
        # for plan in plans:
        #     plan_dict[plan] = plan.features.all()
        try:
            userid = request.user.id
            employer_details = employer.objects.get(user__id=userid)
            eid = employer.objects.get(user__id=userid).id
            isemployer = True
        except ObjectDoesNotExist:
            isemployer = False
        context = {
            'princing': subscription_plan.objects.all().order_by('price'),
            # 'plan_dict':plan_dict,
            'allemployers': employers.filter(public_company_info='Y', is_verified=True)[:20],
            'employer_details': employer_details,
            'isemployer': isemployer,
            'activeUsersCount': active_users_count,
            'candidates_count': candidates_count,
            'employers_count': employers_count,
            'jobs_count': jobs_count,
            'users': users,
            'employers': employers,
            'candidates': candidates,
            'users_count': users_count,
            'ip_adresse': ip_adresse,
        }
        return render(request, 'index.html', context=context)


def about(request):
    reader = geoip2.database.Reader(
        './static/GeoLite2-City/GeoLite2-City.mmdb')
    ip_adresse = get_client_ip(request)
    res = reader.city(ip_adresse)
    country = res.country.name
    context = {
        'res': res,
        'ip_adresse': ip_adresse,
    }
    return render(request, 'about.html', context)


def terms(request):
    return render(request, 'terms.html')


def jobdetails(request):
    return render(request, 'job-details.html')


def privacypolicy(request):
    return render(request, 'privacy-policy.html')


def termsconditions(request):
    return render(request, 'terms-conditions.html')
