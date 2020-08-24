from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/page=<int:page>', views.profile, name='profile_page'),
    path('register', views.SignUpView.as_view(), name='register'),
]
