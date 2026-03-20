from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payroll
from .serializers import PayrollSerializer


class PayrollListCreateView(generics.ListCreateAPIView):
    queryset = Payroll.objects.all().order_by('-year', '-month')
    serializer_class = PayrollSerializer


class PayrollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer


class PayrollMarkPaidView(APIView):
    def post(self, request, pk):
        try:
            payroll = Payroll.objects.get(pk=pk)
        except Payroll.DoesNotExist:
            return Response({'error': 'Payroll record not found'}, status=404)
        payroll.status = 'Paid'
        payroll.save()
        return Response({'message': 'Marked as Paid'})
