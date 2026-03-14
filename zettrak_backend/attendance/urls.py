from django.urls import path
from .views import CheckInView, CheckOutView, AttendanceHistoryView

urlpatterns = [
    path('check-in/', CheckInView.as_view(), name='check_in'),
    path('check-out/', CheckOutView.as_view(), name='check_out'),
    path('history/', AttendanceHistoryView.as_view(), name='attendance_history'),
]