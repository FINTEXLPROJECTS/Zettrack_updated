from django.urls import path
from .views import (
    EmployeeListCreateView, EmployeeRetrieveUpdateView,
    DepartmentListCreateView, DepartmentDetailView,
    DesignationListCreateView, DesignationDetailView,
)

urlpatterns = [
    path('', EmployeeListCreateView.as_view(), name='employee_list_create'),
    path('<int:pk>/', EmployeeRetrieveUpdateView.as_view(), name='employee_detail_update'),

    path('departments/', DepartmentListCreateView.as_view(), name='department_list_create'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department_detail'),

    path('designations/', DesignationListCreateView.as_view(), name='designation_list_create'),
    path('designations/<int:pk>/', DesignationDetailView.as_view(), name='designation_detail'),
]
