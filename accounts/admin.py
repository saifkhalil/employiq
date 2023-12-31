from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'email', 'firstname', 'lastname',
                    'is_candidate', 'is_employer', 'is_verified', 'is_blocked', 'created_at')
    list_filter = ('is_candidate', 'is_employer',
                   'is_verified', 'is_blocked', 'is_superuser')
    search_fields = ('email', 'firstname', 'lastname')


admin.site.register(User, UserAdmin)
