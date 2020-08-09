from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from . import models

# Create your views here.


def index(request):
    if request.method == 'POST':
        tests = models.Test.objects.filter(title__icontains=request.POST['query'])
    else:
        tests = models.Test.objects.all()

    return render(request, 'main/index.html', {'tests': tests})


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'registration/profile.html',
                      {'user': request.user,
                       'results': models.Result.objects.filter(user=request.user)})
    return HttpResponseRedirect(reverse('login'))


def result(request, pk: int):
    return render(request, 'main/result.html', {'res': models.Result.objects.get(id=pk)})


def test_passing(request, pk: int):
    if request.method == 'POST':
        current_answers = list(x for x in request.POST if x[0] in '123456789')
        questions = models.Question.objects.filter(test=pk)
        res = 0
        for question in questions:
            id_answers = set(x.id for x in models.Answer.objects.filter(question=question, is_correct=True))
            current_ids = set(int(x.split('-')[1]) for x in current_answers if x.startswith(str(question.id)))
            if id_answers == current_ids:
                res += 1

        test_result = models.Result(test=models.Test.objects.get(id=pk), user=request.user,
                      count_questions=len(questions), count_correct_questions=res)
        test_result.save()

        return HttpResponseRedirect(reverse('result', args=[test_result.id]))

    try:
        test = models.Test.objects.get(id=pk)
        questions = [(q, models.Answer.objects.filter(question=q))
                     for q in models.Question.objects.filter(test=test)]
        return render(request, 'main/test.html',
                      {'is_auth': request.user.is_authenticated,
                       'questions': questions,
                       'test': test})
    except Exception as e:
        print(e)
        raise Http404


def new_test(request):
    if request.method == "POST":
        try:
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
        except Exception:
            raise Http404

    return render(request, 'main/new_test.html')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
