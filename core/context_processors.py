from accounts.models import User
from candidate.models import candidate
from employer.models import employer, job

def dashboard_counts(request):
    active_users_count = User.objects.filter(is_verified=True).count()
    candidates_count = candidate.objects.all().count()
    employers_count = employer.objects.all().count()
    jobs_count = job.objects.all().count()
    users_count = User.objects.all().count()
    context = {
        'active_users_count': active_users_count,
        'candidates_count': candidates_count,
        'employers_count': employers_count,
        'jobs_count': jobs_count,
        'users_count': users_count,
    }
    return context