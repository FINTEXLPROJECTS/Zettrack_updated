from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView


from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    login_page,
    dashboard_page,
    employees_page,
    attendance_page,
    leaves_page,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_api'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', login_page, name='login_page'),
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('employees-page/', employees_page, name='employees_page'),
    path('attendance-page/', attendance_page, name='attendance_page'),
    path('leaves-page/', leaves_page, name='leaves_page'),
]