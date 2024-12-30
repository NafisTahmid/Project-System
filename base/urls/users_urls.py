from django.urls import path
from base.views import users_views as views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('<str:pk>/', views.getUserDetails, name="user_details"),
    path('register/', views.registerUser, name='register-user'),
    path('update/<str:pk>/', views.updateUserProfileDetails, name='update-user-profile'),
    path('login/', views.loginUser, name="login-user"),
    path('delete/<str:pk>/', views.deleteUser, name="delete-user")
]