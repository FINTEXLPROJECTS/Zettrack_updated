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

    # Users & Roles API
    path('api/v1/accounts/', include('accounts.api_urls')),

    # Employees, Departments, Designations API
    path('api/v1/employees/', include('employees.urls')),

    # Attendance API
    path('api/v1/attendance/', include('attendance.urls')),

    # Leaves API
    path('api/v1/leaves/', include('leave_management.urls')),

    # Companies API
    path('api/v1/companies/', include('companies.urls')),

    # Payroll API
    path('api/v1/payroll/', include('payroll.urls')),

    # Notifications API
    path('api/v1/notifications/', include('notifications.urls')),

    # Reports API
    path('api/v1/reports/', include('reports.urls')),
]
