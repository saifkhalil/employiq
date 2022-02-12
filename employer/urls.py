from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('', login_required(my_employer_details), name='my_employer_details'),
    path('create', login_required(
        EmployerCreateView.as_view()), name='employer_create'),
    path('<uuid:eid>', login_required(
        employer_details), name='employer_details'),
    path('job/create', login_required(
        JobCreateView.as_view()), name='job_create'),
    path('job/<uuid:jid>', login_required(
        JobDetails), name='job_details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
