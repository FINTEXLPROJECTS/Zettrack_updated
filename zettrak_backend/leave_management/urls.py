from django.urls import path
from .views import (
    LeaveApplyView, LeaveHistoryView, LeaveBalanceView,
    LeaveApproveView, LeaveRejectView,
    LeaveTypeListCreateView, LeaveTypeDetailView,
)

urlpatterns = [
    # Existing endpoints (unchanged)
    path('apply/', LeaveApplyView.as_view(), name='leave_apply'),
    path('history/', LeaveHistoryView.as_view(), name='leave_history'),
    path('balance/', LeaveBalanceView.as_view(), name='leave_balance'),
    path('<int:pk>/approve/', LeaveApproveView.as_view(), name='leave_approve'),
    path('<int:pk>/reject/', LeaveRejectView.as_view(), name='leave_reject'),

    # New LeaveType endpoints
    path('types/', LeaveTypeListCreateView.as_view(), name='leave_type_list'),
    path('types/<int:pk>/', LeaveTypeDetailView.as_view(), name='leave_type_detail'),
]
