from rest_framework.views import APIView
from rest_framework.response import Response
from employees.models import Employee
from attendance.models import Attendance
from leave_management.models import LeaveRequest
from payroll.models import Payroll


class ReportSummaryView(APIView):
    def get(self, request):
        total_employees = Employee.objects.count()
        active_employees = Employee.objects.filter(is_active=True).count()
        total_attendance = Attendance.objects.count()
        total_leaves = LeaveRequest.objects.count()
        approved_leaves = LeaveRequest.objects.filter(status='Approved').count()
        pending_leaves = LeaveRequest.objects.filter(status='Pending').count()
        rejected_leaves = LeaveRequest.objects.filter(status='Rejected').count()
        total_payroll = Payroll.objects.count()
        paid_payroll = Payroll.objects.filter(status='Paid').count()
        pending_payroll = Payroll.objects.filter(status='Pending').count()

        return Response({
            'employees': {
                'total': total_employees,
                'active': active_employees,
                'inactive': total_employees - active_employees,
            },
            'attendance': {
                'total_records': total_attendance,
            },
            'leaves': {
                'total': total_leaves,
                'approved': approved_leaves,
                'pending': pending_leaves,
                'rejected': rejected_leaves,
            },
            'payroll': {
                'total': total_payroll,
                'paid': paid_payroll,
                'pending': pending_payroll,
            },
        })
