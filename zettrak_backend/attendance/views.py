from django.shortcuts import render

# Create your views here.
from datetime import date
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Attendance
from .serializers import AttendanceSerializer
from employees.models import Employee


class CheckInView(APIView):
    def post(self, request):
        employee_id = request.data.get('employee')
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=404)

        today = date.today()
        if Attendance.objects.filter(employee=employee, date=today).exists():
            return Response({'error': 'Already checked in today'}, status=400)

        record = Attendance.objects.create(
            employee=employee,
            date=today,
            check_in=timezone.now(),
            status='Present'
        )
        return Response(AttendanceSerializer(record).data, status=201)


class CheckOutView(APIView):
    def post(self, request):
        employee_id = request.data.get('employee')
        try:
            employee = Employee.objects.get(id=employee_id)
            record = Attendance.objects.get(employee=employee, date=date.today())
        except (Employee.DoesNotExist, Attendance.DoesNotExist):
            return Response({'error': 'Attendance record not found'}, status=404)

        if record.check_out:
            return Response({'error': 'Already checked out'}, status=400)

        record.check_out = timezone.now()
        record.save()
        return Response(AttendanceSerializer(record).data)


class AttendanceHistoryView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()