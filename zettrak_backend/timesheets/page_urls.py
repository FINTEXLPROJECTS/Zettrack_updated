from django.urls import path
from . import views

urlpatterns = [
    path('admin-timesheets-page/', views.admin_timesheet_page, name='admin_timesheet_page'),
    path('customer-timesheets/', views.customer_timesheet_page, name='customer_timesheet_page'),
]
