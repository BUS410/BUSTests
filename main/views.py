from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import models

# Create your views here.


def index(request, query=''):
    if request.method == 'POST':
        tests = models.Test.objects.filter(title__icontains=request.POST['query'])
    else:
        tests = models.Test.objects.filter(title__icontains=query)

    return render(request, 'main/index.html', {'tests': tests})


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'registration/profile.html', {'user': request.user})
    return HttpResponseRedirect(reverse('login'))


def new_test(request):
    if request.method == "POST":
        title = request.POST['title']
        count_questions = sum(1 for key in request.POST if key.endswith('0'))
        test = models.Test(title=title)
        test.save()
        for i in range(1, count_questions + 1):
            question = models.Question(test=test, text=request.POST[f'{i}-0'])
            question.save()
            count_answers = sum(1 for key in request.POST if key.split('-')[0] == str(i)) - 1
            for j in range(1, count_answers + 1):
                answer = models.Answer(text=request.POST[f'{i}-{j}'], question=question,
                                       is_correct=f'!{i}-{j}' in request.POST)
                answer.save()
        return HttpResponseRedirect(reverse('new_test'))

    return render(request, 'main/new_test.html')
