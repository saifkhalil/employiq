from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('', login_required(candlist), name='candlist'),
    #     path('pdf', login_required(pdf), name='pdf'),
    path('pdf', login_required(generate_pdf), name='generate_pdf'),
    path('view_pdf', login_required(view_pdf), name='view_pdf'),
    path('create', login_required(
        CandidateCreateView.as_view()), name='candidate_create'),
    path('<uuid:pk>/update/',
         login_required(CandidateUpdateView.as_view()), name='candidate_update'),
    path('<uuid:cid>', login_required(candetials), name='candetials'),
    path('education/delete/<uuid:eid>',
         login_required(del_education), name='del_education'),
    path('education/new', login_required(EducationCreateView.as_view()),
         name='educationnew'),
    path('education/create', login_required(EducationCreateView.as_view()),
         name='educationcreate'),
    path('education/<uuid:pk>/update/',
         login_required(EducationUpdateView.as_view()), name='education_update'),
    path('employment/create', login_required(EmploymentCreateView.as_view()),
         name='employmentcreate'),
    path('employement/<uuid:pk>/update/',
         login_required(EmploymentUpdateView.as_view()), name='employement_update'),
    path('employement/<uuid:eid>/delete/',
         login_required(del_employement), name='del_employement'),
    path('language/create', login_required(LanguageCreateView.as_view()),
         name='languagecreate'),
    path('language/createBS/',
         login_required(LanguageCreateView.as_view()), name='create_Lang_BS'),
    path('language/<uuid:pk>/update/',
         login_required(LanguageUpdateView.as_view()), name='language_update'),
    path('language/<uuid:eid>/delete/',
         login_required(del_language), name='del_language'),
    path('certificate/create', login_required(CertificateCreateView.as_view()),
         name='certificatecreate'),
    path('certificate/<uuid:pk>/update/',
         login_required(CertificateUpdateView.as_view()), name='certificate_update'),
    path('certificate/<uuid:eid>/delete/',
         login_required(del_certificate), name='del_certificate'),
    path('myprofile', login_required(my_candidate_details),
         name='my_candidate_details'),
    # path('<uuid:pk>', login_required(CandidateDetail.as_view()),name = 'my_candidate'),
    #path('pdf/', GeneratePdf.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
