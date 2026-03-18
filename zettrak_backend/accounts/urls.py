from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    CustomerLoginView,
    home_page,
    about_page,
    contact_page,
    login_page,
    dashboard_page,
    employees_page,
    attendance_page,
    leaves_page,
    leave_history_page,
    customer_dashboard_page,
    users_page,
    roles_page,
    companies_page,
    leave_types_page,
    leave_balances_page,
)

urlpatterns = [
    # API endpoints
    path('login/', LoginView.as_view(), name='login_api'),
    path('customer-login/', CustomerLoginView.as_view(), name='customer_login_api'),
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
    path('customer-dashboard/', customer_dashboard_page, name='customer_dashboard_page'),

    # New management pages
    path('users-page/', users_page, name='users_page'),
    path('roles-page/', roles_page, name='roles_page'),
    path('companies-page/', companies_page, name='companies_page'),
    path('leave-types-page/', leave_types_page, name='leave_types_page'),
    path('leave-balances-page/', leave_balances_page, name='leave_balances_page'),
]
