from math import ceil

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from . import models


# Create your views here.


ELEMENT_IN_PAGE = 10


def index(request, page=1, q=''):
    if request.method == 'POST':
        tests = models.Test.objects.filter(title__icontains=request.POST['query']).order_by('-id')
        q = request.POST['query']
    elif q:
        tests = models.Test.objects.filter(title__icontains=q).order_by('-id')
    else:
        tests = models.Test.objects.order_by('-id')

    count_pages = ceil(len(tests) / ELEMENT_IN_PAGE)
    tests = tests[(page - 1) * ELEMENT_IN_PAGE:page * ELEMENT_IN_PAGE]

    return render(request, 'main/index.html',
                  {'tests': tests, 'pages': range(1, count_pages + 1) if count_pages > 1 else False,
                   'query': q})


def result(request, pk: int):
    try:
        res = models.Result.objects.get(id=pk)
        percent = round(res.count_correct_questions / res.count_questions * 100, 2)
        print(res.count_correct_questions, res.count_questions)
        return render(request, 'main/result.html', {'res': res, 'percent': percent})
    except Exception as e:
        print(e)
        raise Http404


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

        test_result = models.Result(test=models.Test.objects.get(id=pk),
                                    count_questions=len(questions), count_correct_questions=res,
                                    attempt=len(models.Result.objects.filter(user=request.user, test_id=pk))+1
                                    if request.user.is_authenticated else 1)
        if request.user.is_authenticated:
            test_result.user = request.user
        test_result.save()

        return HttpResponseRedirect(reverse('result', args=[test_result.id]))

    try:
        test = models.Test.objects.get(id=pk)
        questions = [(q, models.Answer.objects.filter(question=q))
                     for q in models.Question.objects.filter(test=test)]
        return render(request, 'main/test.html',
                      {'questions': questions,
                       'test': test,
                       'count_passed': len(models.Result.objects.filter(test=test))})
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
            return HttpResponseRedirect(reverse('test_list'))
        except Exception:
            raise Http404

    return render(request, 'main/new_test.html')


def results_by_test(request, pk, page=1):
    try:
        test = models.Test.objects.get(id=pk)
    except Exception as e:
        print(e)
        raise Http404
    results = models.Result.objects.filter(test=test).order_by('-id')

    count_pages = ceil(len(results) / ELEMENT_IN_PAGE)
    results = results[(page - 1) * ELEMENT_IN_PAGE:page * ELEMENT_IN_PAGE]

    return render(request, 'main/results.html', {
        'pages': range(1, count_pages + 1) if count_pages > 1 else False,
        'test': test,
        'results': results,
    })
