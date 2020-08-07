from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/profile', views.profile, name='profile'),
    path('new_test', views.new_test, name='new_test')
]