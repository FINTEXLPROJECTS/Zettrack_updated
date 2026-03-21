from django.urls import path
from . import views

urlpatterns = [
    # Projects
    path('projects/', views.ProjectListCreateView.as_view(), name='project_list_create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),

    # Timesheets CRUD
    path('', views.TimesheetListCreateView.as_view(), name='timesheet_list_create'),
    path('<int:pk>/', views.TimesheetDetailView.as_view(), name='timesheet_detail'),

    # Status actions
    path('<int:pk>/submit/', views.TimesheetSubmitView.as_view(), name='timesheet_submit'),
    path('<int:pk>/approve/', views.TimesheetApproveView.as_view(), name='timesheet_approve'),
    path('<int:pk>/reject/', views.TimesheetRejectView.as_view(), name='timesheet_reject'),

    # Bulk actions (admin)
    path('bulk-action/', views.TimesheetBulkActionView.as_view(), name='timesheet_bulk_action'),
]
