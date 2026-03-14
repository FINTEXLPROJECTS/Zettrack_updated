from django.urls import path
from .views import EmployeeListCreateView, EmployeeRetrieveUpdateView

urlpatterns = [
    path('', EmployeeListCreateView.as_view(), name='employee_list_create'),
    path('<int:pk>/', EmployeeRetrieveUpdateView.as_view(), name='employee_detail_update'),
]