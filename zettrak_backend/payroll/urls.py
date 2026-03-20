from django.urls import path
from .views import PayrollListCreateView, PayrollDetailView, PayrollMarkPaidView

urlpatterns = [
    path('', PayrollListCreateView.as_view(), name='payroll_list_create'),
    path('<int:pk>/', PayrollDetailView.as_view(), name='payroll_detail'),
    path('<int:pk>/mark-paid/', PayrollMarkPaidView.as_view(), name='payroll_mark_paid'),
]
