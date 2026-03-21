from rest_framework import serializers
from .models import Project, Timesheet


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TimesheetSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField(read_only=True)
    project_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Timesheet
        fields = [
            'id', 'employee', 'employee_name', 'project', 'project_name',
            'date', 'hours', 'task_description', 'is_billable',
            'status', 'rejection_reason',
            'created_by', 'updated_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['status', 'rejection_reason', 'created_by', 'updated_by', 'created_at', 'updated_at']

    def get_employee_name(self, obj):
        return str(obj.employee)

    def get_project_name(self, obj):
        return obj.project.name


class TimesheetAdminSerializer(serializers.ModelSerializer):
    """Admin can edit all fields including status."""
    employee_name = serializers.SerializerMethodField(read_only=True)
    project_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Timesheet
        fields = '__all__'

    def get_employee_name(self, obj):
        return str(obj.employee)

    def get_project_name(self, obj):
        return obj.project.name
