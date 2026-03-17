from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LeaveRequest, LeaveBalance, LeaveType
from .serializers import LeaveRequestSerializer, LeaveBalanceSerializer, LeaveTypeSerializer


# ── Existing views (unchanged) ──

class LeaveApplyView(generics.CreateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer


class LeaveHistoryView(generics.ListAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer


class LeaveBalanceView(generics.ListAPIView):
    queryset = LeaveBalance.objects.all()
    serializer_class = LeaveBalanceSerializer


class LeaveApproveView(APIView):
    def post(self, request, pk):
        try:
            leave = LeaveRequest.objects.get(pk=pk)
        except LeaveRequest.DoesNotExist:
            return Response({'error': 'Leave request not found'}, status=404)

        leave.status = 'Approved'
        leave.save()
        return Response({'message': 'Leave approved'})


class LeaveRejectView(APIView):
    def post(self, request, pk):
        try:
            leave = LeaveRequest.objects.get(pk=pk)
        except LeaveRequest.DoesNotExist:
            return Response({'error': 'Leave request not found'}, status=404)

        leave.status = 'Rejected'
        leave.save()
        return Response({'message': 'Leave rejected'})


# ── New LeaveType CRUD views ──

class LeaveTypeListCreateView(generics.ListCreateAPIView):
    queryset = LeaveType.objects.all().order_by('id')
    serializer_class = LeaveTypeSerializer


class LeaveTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
