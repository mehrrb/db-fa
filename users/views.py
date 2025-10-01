from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileSerializer, UserSerializer


class UserLoginView(APIView):
    """API view for user authentication and login."""

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user_id": user.id, "username": user.username}
            )
        return Response(
            {"error": "نام کاربری یا رمز عبور اشتباه است"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class UserLogoutView(APIView):
    """API view for logging out user."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"message": "خروج با موفقیت انجام شد"}, status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for managing users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Override permissions:
        - Allow anyone to register (create)
        - Only admin users can list all users
        - Users can view and update their own profiles
        """
        if self.action == "create":
            permission_classes = [AllowAny]
        elif self.action == "list":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Filter queryset for non-admin users to see only their own data."""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class ProfileViewSet(viewsets.ModelViewSet):
    """Viewset for managing profiles."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset for non-admin users to see only their own data."""
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)


# Legacy views for template-based access
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def login_view(request: HttpRequest) -> Response:
    """Legacy view for user authentication and login."""
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

    return Response(
        {"detail": "Please provide credentials"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request: HttpRequest) -> Response:
    """Legacy view for logging out user."""
    logout(request)
    return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_view(request: HttpRequest) -> Response:
    """Legacy view for user dashboard."""
    return Response({"detail": "Dashboard accessed"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAdminUser])
def register_view(request: HttpRequest) -> Response:
    """Legacy view for registering new users."""
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Register page accessed"}, status=status.HTTP_200_OK)
