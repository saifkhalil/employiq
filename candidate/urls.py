from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(candlist), name='candlist'),
    path('<int:cid>', login_required(candetials), name='candetials'),
    path('education/delete/<int:eid>',
         login_required(del_education), name='del_education'),
    path('education/new', login_required(EducationCreateView.as_view()),
         name='educationnew'),
    path('education/create', login_required(EducationCreateView.as_view()),
         name='educationcreate'),
    path('education/<int:pk>/update/',
         login_required(EducationUpdateView.as_view()), name='education_update'),
    path('employment/create', login_required(EmploymentCreateView.as_view()),
         name='employmentcreate'),
    path('employement/<int:pk>/update/',
         login_required(EmploymentUpdateView.as_view()), name='employement_update'),
    path('employement/delete/<int:eid>',
         login_required(del_employement), name='del_employement'),
    path('myprofile', login_required(my_candidate_details),
         name='my_candidate_details'),
    path('pdf/', GeneratePdf.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
