from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from .models import Project, Timesheet
from .serializers import ProjectSerializer, TimesheetSerializer, TimesheetAdminSerializer


# ─── Template page views ───────────────────────────────────────────────────────

def admin_timesheet_page(request):
    return render(request, 'admin_timesheets.html')


def customer_timesheet_page(request):
    return render(request, 'customer_timesheets.html')


# ─── Project CRUD (Admin only) ─────────────────────────────────────────────────

class ProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(is_active=True)
        return Response(ProjectSerializer(projects, many=True).data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Admin only'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Project, pk=pk)

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Admin only'}, status=status.HTTP_403_FORBIDDEN)
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Admin only'}, status=status.HTTP_403_FORBIDDEN)
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Employee Timesheet CRUD ───────────────────────────────────────────────────

class TimesheetListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            # Admin: filter by employee, project, date, status
            qs = Timesheet.objects.all()
            emp = request.query_params.get('employee')
            proj = request.query_params.get('project')
            dt = request.query_params.get('date')
            st = request.query_params.get('status')
            if emp:
                qs = qs.filter(employee_id=emp)
            if proj:
                qs = qs.filter(project_id=proj)
            if dt:
                qs = qs.filter(date=dt)
            if st:
                qs = qs.filter(status=st)
            return Response(TimesheetAdminSerializer(qs, many=True).data)
        else:
            # Employee: own timesheets only
            try:
                employee = request.user.employee_profile
            except Exception:
                return Response({'error': 'Employee profile not found'}, status=status.HTTP_404_NOT_FOUND)
            qs = Timesheet.objects.filter(employee=employee)
            return Response(TimesheetSerializer(qs, many=True).data)

    def post(self, request):
        try:
            employee = request.user.employee_profile
        except Exception:
            return Response({'error': 'Employee profile not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['employee'] = employee.id

        serializer = TimesheetSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                employee=employee,
                created_by=request.user,
                status=Timesheet.STATUS_DRAFT
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimesheetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        ts = get_object_or_404(Timesheet, pk=pk)
        if not user.is_staff:
            try:
                emp = user.employee_profile
                if ts.employee != emp:
                    return None
            except Exception:
                return None
        return ts

    def put(self, request, pk):
        ts = self.get_object(pk, request.user)
        if ts is None:
            return Response({'error': 'Not found or forbidden'}, status=status.HTTP_403_FORBIDDEN)

        # Employees cannot edit submitted/approved timesheets
        if not request.user.is_staff and ts.status != Timesheet.STATUS_DRAFT:
            return Response({'error': 'Cannot edit after submission'}, status=status.HTTP_400_BAD_REQUEST)

        SerializerClass = TimesheetAdminSerializer if request.user.is_staff else TimesheetSerializer
        serializer = SerializerClass(ts, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ts = self.get_object(pk, request.user)
        if ts is None:
            return Response({'error': 'Not found or forbidden'}, status=status.HTTP_403_FORBIDDEN)
        if not request.user.is_staff and ts.status != Timesheet.STATUS_DRAFT:
            return Response({'error': 'Cannot delete after submission'}, status=status.HTTP_400_BAD_REQUEST)
        ts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Submit (Employee action) ──────────────────────────────────────────────────

class TimesheetSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        ts = get_object_or_404(Timesheet, pk=pk)
        try:
            emp = request.user.employee_profile
            if ts.employee != emp:
                return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({'error': 'Employee profile not found'}, status=status.HTTP_404_NOT_FOUND)

        if ts.status != Timesheet.STATUS_DRAFT:
            return Response({'error': 'Only draft timesheets can be submitted'}, status=status.HTTP_400_BAD_REQUEST)

        ts.status = Timesheet.STATUS_SUBMITTED
        ts.updated_by = request.user
        ts.save()
        return Response({'message': 'Timesheet submitted successfully', 'status': ts.status})


# ─── Approve / Reject (Admin & Manager) ───────────────────────────────────────

class TimesheetApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Admin only'}, status=status.HTTP_403_FORBIDDEN)
        ts = get_object_or_404(Timesheet, pk=pk)
        if ts.status != Timesheet.STATUS_SUBMITTED:
            return Response({'error': 'Only submitted timesheets can be approved'}, status=status.HTTP_400_BAD_REQUEST)
        ts.status = Timesheet.STATUS_APPROVED
        ts.updated_by = request.user
        ts.rejection_reason = None
        ts.save()
        return Response({'message': 'Timesheet approved', 'status': ts.status})


class TimesheetRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Admin only'}, status=status.HTTP_403_FORBIDDEN)
        ts = get_object_or_404(Timesheet, pk=pk)
        if ts.status != Timesheet.STATUS_SUBMITTED:
            return Response({'error': 'Only submitted timesheets can be rejected'}, status=status.HTTP_400_BAD_REQUEST)
        reason = request.data.get('rejection_reason', '')
        if not reason:
            return Response({'error': 'Rejection reason is required'}, status=status.HTTP_400_BAD_REQUEST)
        ts.status = Timesheet.STATUS_REJECTED
        ts.rejection_reason = reason
        ts.updated_by = request.user
        ts.save()
        return Response({'message': 'Timesheet rejected', 'status': ts.status})


# ─── Bulk Approve / Reject (Admin) ────────────────────────────────────────────

class TimesheetBulkActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Admin only'}, status=status.HTTP_403_FORBIDDEN)
        action = request.data.get('action')  # 'approve' or 'reject'
        ids = request.data.get('ids', [])
        reason = request.data.get('rejection_reason', '')

        if action not in ['approve', 'reject']:
            return Response({'error': 'action must be approve or reject'}, status=status.HTTP_400_BAD_REQUEST)
        if action == 'reject' and not reason:
            return Response({'error': 'Rejection reason required'}, status=status.HTTP_400_BAD_REQUEST)

        qs = Timesheet.objects.filter(id__in=ids, status=Timesheet.STATUS_SUBMITTED)
        count = qs.count()
        if action == 'approve':
            qs.update(status=Timesheet.STATUS_APPROVED, updated_by=request.user, rejection_reason=None)
        else:
            qs.update(status=Timesheet.STATUS_REJECTED, rejection_reason=reason, updated_by=request.user)

        return Response({'message': f'{count} timesheets {action}d successfully'})
