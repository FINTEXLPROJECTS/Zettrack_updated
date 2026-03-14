from django.urls import path
from .views import LeaveApplyView, LeaveHistoryView, LeaveBalanceView, LeaveApproveView, LeaveRejectView

urlpatterns = [
    path('apply/', LeaveApplyView.as_view(), name='leave_apply'),
    path('history/', LeaveHistoryView.as_view(), name='leave_history'),
    path('balance/', LeaveBalanceView.as_view(), name='leave_balance'),
    path('<int:pk>/approve/', LeaveApproveView.as_view(), name='leave_approve'),
    path('<int:pk>/reject/', LeaveRejectView.as_view(), name='leave_reject'),
]