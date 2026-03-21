from django.contrib import admin
from .models import Project, Timesheet


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'is_active', 'created_at']
    list_filter = ['company', 'is_active']
    search_fields = ['name']


@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ['employee', 'project', 'date', 'hours', 'is_billable', 'status', 'created_at']
    list_filter = ['status', 'is_billable', 'project', 'date']
    search_fields = ['employee__first_name', 'employee__last_name', 'project__name', 'task_description']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
