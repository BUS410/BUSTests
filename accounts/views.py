from math import ceil

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from main import models
from .forms import SignUpForm


# Create your views here.


ELEMENT_IN_PAGE = 20


def profile(request, page=1):
    if request.user.is_authenticated:
        results = models.Result.objects.filter(user=request.user).order_by('-id')
        count_pages = ceil(len(results) / ELEMENT_IN_PAGE)
        results = results[(page - 1) * ELEMENT_IN_PAGE:page * ELEMENT_IN_PAGE]
        return render(request, 'registration/profile.html',
                      {'user': request.user,
                       'results': results,
                       'pages': range(1, count_pages + 1) if count_pages > 1 else False})

    return HttpResponseRedirect(reverse('login'))


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
