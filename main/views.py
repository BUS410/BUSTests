from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import models

# Create your views here.


def index(request):
    tests = models.Test.objects.all()
    return render(request, 'main/index.html', {'tests': tests})


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'registration/profile.html', {'user': request.user})
    return HttpResponseRedirect(reverse('login'))
