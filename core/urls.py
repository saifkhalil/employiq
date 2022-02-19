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
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('', views.home, name='home'),
    path('accounts/', include('allauth.urls')),
    # path('after', views.after, name='after'),
    path('about', views.about, name='about'),
    path('language_setting', include('rosetta.urls')),
    path('candidates/', include('candidate.urls'), name='candidate'),
    path('employer/', include('employer.urls'), name='employer'),
    path('job-details', views.jobdetails, name='job-details'),
    path('privacy-policy', views.privacypolicy, name='privacy-policy'),
    path('terms-conditions', views.termsconditions, name='terms-conditions'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
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
