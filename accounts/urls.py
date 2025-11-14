from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, LogoutView, ProfileView, ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/me/', ProfileView.as_view(), name='profile_me'),  # Alias for profile/
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
