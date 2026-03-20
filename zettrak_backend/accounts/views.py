from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserSerializer, RoleSerializer
from .models import User, Role


# ── Public pages (no login required) ──

def home_page(request):
    return render(request, 'home.html')


def about_page(request):
    return render(request, 'about.html')


def contact_page(request):
    return render(request, 'contact.html')


# ── Auth page ──

def login_page(request):
    return render(request, 'login.html')


# ── Admin panel pages ──

def dashboard_page(request):
    return render(request, 'dashboard.html')


def employees_page(request):
    return render(request, 'employees.html')


def attendance_page(request):
    return render(request, 'attendance.html')


def leaves_page(request):
    return render(request, 'leaves.html')


def leave_history_page(request):
    return render(request, 'leave_history.html')


def customer_dashboard_page(request):
    return render(request, 'customer_dashboard.html')


def users_page(request):
    return render(request, 'users.html')


def roles_page(request):
    return render(request, 'roles.html')


def companies_page(request):
    return render(request, 'companies.html')


def leave_types_page(request):
    return render(request, 'leave_types.html')


def leave_balances_page(request):
    return render(request, 'leave_balances.html')


def departments_page(request):
    return render(request, 'departments.html')


def designations_page(request):
    return render(request, 'designations.html')


def payroll_page(request):
    return render(request, 'payroll.html')


def notifications_page(request):
    return render(request, 'notifications.html')


def reports_page(request):
    return render(request, 'reports.html')


def profile_page(request):
    return render(request, 'profile.html')


# ── Customer-only pages (employee portal) ──

def customer_attendance_page(request):
    return render(request, 'customer_attendance.html')


def customer_leaves_page(request):
    return render(request, 'customer_leaves.html')


def customer_leave_history_page(request):
    return render(request, 'customer_leave_history.html')


# ── Auth API ──

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Login successful',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
            }
        }, status=status.HTTP_200_OK)


# ── Customer Login (email + phone) ──

class CustomerLoginView(APIView):
    permission_classes = []

    def post(self, request):
        from employees.models import Employee  # lazy import to avoid circular dependency

        email = request.data.get('email', '').strip()
        phone = request.data.get('phone', '').strip()

        if not email or not phone:
            return Response(
                {'error': 'Email and mobile number are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            employee = Employee.objects.select_related('user', 'company').get(
                email=email, phone=phone, is_active=True
            )
        except Employee.DoesNotExist:
            return Response(
                {'error': 'No active employee found with these credentials. Please contact your admin.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Employee.MultipleObjectsReturned:
            return Response(
                {'error': 'Multiple records found. Please contact your admin.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = employee.user
        if not user.is_active:
            return Response(
                {'error': 'Your account is inactive. Please contact admin.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Login successful',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
            },
            'employee': {
                'id': employee.id,
                'employee_code': employee.employee_code,
                'first_name': employee.first_name,
                'last_name': employee.last_name or '',
                'full_name': f"{employee.first_name} {employee.last_name or ''}".strip(),
                'email': employee.email,
                'phone': employee.phone,
                'date_of_joining': str(employee.date_of_joining),
                'company_name': employee.company.name if employee.company else '',
            }
        }, status=status.HTTP_200_OK)


# ── Users API ──

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ── Roles API ──

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# ── My Profile API ──

class MyProfileView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
