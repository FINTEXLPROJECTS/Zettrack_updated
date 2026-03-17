from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    home_page,
    about_page,
    contact_page,
    login_page,
    dashboard_page,
    employees_page,
    attendance_page,
    leaves_page,
    leave_history_page,
)

urlpatterns = [
    # API endpoints
    path('login/', LoginView.as_view(), name='login_api'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Public pages (no login required)
    path('', home_page, name='home_page'),
    path('about/', about_page, name='about_page'),
    path('contact/', contact_page, name='contact_page'),

    # Auth page
    path('login-page/', login_page, name='login_page'),

    # Admin panel pages
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('employees-page/', employees_page, name='employees_page'),
    path('attendance-page/', attendance_page, name='attendance_page'),
    path('leaves-page/', leaves_page, name='leaves_page'),
    path('leave-history-page/', leave_history_page, name='leave_history_page'),
]
