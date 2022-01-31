from django.shortcuts import render, get_object_or_404, redirect


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def jobdetails(request):
    return render(request, 'job-details.html')


def privacypolicy(request):
    return render(request, 'privacy-policy.html')


def termsconditions(request):
    return render(request, 'terms-conditions.html')
