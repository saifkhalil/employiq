from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token

from accounts.forms import RegistrationForm, UserAuthenticationForm, UserUpdateForm


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            fullname = "%s %s" % (form.cleaned_data.get(
                'firstname'), form.cleaned_data.get('lastname'))
            phone = str(form.cleaned_data.get('phone'))[1:]
            account = authenticate(request, email=email, password=raw_password)
            token = Token.objects.get(user=account).key
            context['token'] = token
            if account:
                login(request, account)
                return render(request, 'after_register.html', context)
        else:
            context['form'] = form
    else:
        if not request.user.is_authenticated:
            form = RegistrationForm()
            context['form'] = form
        else:
            return render(request, 'after_register.html')
    return render(request, 'account/register copy.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}
    if request.GET.get('next') is None:
        next_page = 'home'
    else:
        next_page = request.GET.get('next')
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect(next_page)
    else:
        form = UserAuthenticationForm()
    context['login_form'] = form
    return render(request, "account/login.html", context)


def account_view(request):
    context = {}
    if request.POST:
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
                "firstname": request.POST['firstname'],
                "lastname": request.POST['lastname'],
                "phone": request.POST['phone'],
            }
            form.save()
            context['success_message'] = "Profile Updated"
    else:
        form = UserUpdateForm(

            initial={
                "email": request.user.email,
                "username": request.user.username,
                "firstname": request.user.firstname,
                "lastname": request.user.lastname,
                "phone": request.user.phone,
            }
        )
    context['account_form'] = form
    return render(request, "account/account.html", context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})
