from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Create a router for DRF ViewSets
router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"profiles", views.ProfileViewSet)

urlpatterns = [
    # API URLs
    path("", include(router.urls)),
    path("login/", views.UserLoginView.as_view(), name="api_login"),
    path("logout/", views.UserLogoutView.as_view(), name="api_logout"),
    # Legacy URLs for template-based access
    path("login-page/", views.login_view, name="login"),
    path("logout-page/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("register/", views.register_view, name="register"),
]
