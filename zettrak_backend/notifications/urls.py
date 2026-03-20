from django.urls import path
from .views import (
    NotificationListCreateView, NotificationDetailView,
    NotificationMarkReadView, NotificationMarkAllReadView,
)

urlpatterns = [
    path('', NotificationListCreateView.as_view(), name='notification_list_create'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification_detail'),
    path('<int:pk>/mark-read/', NotificationMarkReadView.as_view(), name='notification_mark_read'),
    path('mark-all-read/', NotificationMarkAllReadView.as_view(), name='notification_mark_all_read'),
]
