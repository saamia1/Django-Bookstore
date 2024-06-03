
from django.urls import path, include
from .views import RegisterView, UserDetailView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', include('rest_framework.urls'), name='logout'),
    path('profile/', UserDetailView.as_view(), name='profile'),
]
