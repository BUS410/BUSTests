from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='test_list'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/register', views.SignUpView.as_view(), name='register'),
    path('new_test', views.new_test, name='new_test'),
]
