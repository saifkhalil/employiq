"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from accounts.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    active_user,
    must_authenticate_view,
    send_active,
    block_user,
    unblock_user,
    
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import render



def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html')
    response.status_code = 500
    return response


urlpatterns = i18n_patterns(
    path('', views.home, name='home'),
    # path("cookies/", include("cookie_consent.urls")),
    path('dashboard/users', views.users_list, name='dashboard'),
    path('dashboard/users', views.users_list, name='users_list'),
    path('dashboard/employers', views.employers_list, name='employers_list'),
    path('dashboard/candidates', views.candidates_list, name='candidates_list'),
    path('dashboard/suggestions', views.suggestions_list, name='suggestions_list'),
    path('dashboard/subscriptions', views.subscriptions_list,
         name='subscriptions_list'),
    path('dashboard/subscriptions_plan', views.subscriptions_plan_list,
         name='subscriptions_plan_list'),
    path('accounts/', include('allauth.urls')),
    # path('after', views.after, name='after'),
    path('about', views.about, name='about'),
    path('policy-for-terms-of-use', views.terms, name='terms'),
    path('language_setting', include('rosetta.urls')),
    path('candidates/', include('candidate.urls'), name='candidate'),
    path('employer/', include('employer.urls'), name='employer'),
    path('job-details', views.jobdetails, name='job-details'),
    path('privacy-policy', views.privacypolicy, name='privacy-policy'),
    path('terms-conditions', views.termsconditions, name='terms-conditions'),
    path('grappelli/', include('grappelli.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('emadmin/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('verify/<uuid:userid>', send_active, name="send_active"),
    path('block_user/<uuid:userid>', block_user, name="block_user"),
    path('unblock_user/<uuid:userid>', unblock_user, name="unblock_user"),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, }),
    path('register/', registration_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('profile/', login_required(account_view), name="account"),
    path('activate_user/<uidb64>/<token>', active_user, name='active'),
    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html'), name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(html_email_template_name='registration/html_password_reset_email.html'),
         name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
)
