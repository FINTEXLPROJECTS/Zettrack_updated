from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("ZetTrak backend is running successfully")


urlpatterns = [
    path('admin/', admin.site.urls),

    # Template pages + auth API
    path('', include('accounts.urls')),
    path('api/v1/auth/', include('accounts.urls')),

    # New: Users & Roles API
    path('api/v1/accounts/', include('accounts.api_urls')),

    # Existing API routes (unchanged)
    path('api/v1/employees/', include('employees.urls')),
    path('api/v1/attendance/', include('attendance.urls')),
    path('api/v1/leaves/', include('leave_management.urls')),

    # New: Companies API
    path('api/v1/companies/', include('companies.urls')),
]
