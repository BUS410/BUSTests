from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='test_list'),
    path('result/<int:pk>', views.result, name='result'),
    path('test/<int:pk>', views.test_passing, name='test'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/register', views.SignUpView.as_view(), name='register'),
    path('new_test', views.new_test, name='new_test'),
]
