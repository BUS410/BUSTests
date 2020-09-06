from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    title = models.CharField(max_length=120, verbose_name='Заголовок теста')
    note = models.TextField(blank=True, null=True,
                            verbose_name='Примечание к тесту')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Тесты'
        verbose_name = 'тест'


class Question(models.Model):
    text = models.TextField(verbose_name='Текст вопроса')
    test = models.ForeignKey(Test, on_delete=models.CASCADE,
                             verbose_name='Тест')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = 'вопрос'
        ordering = ('test',)


class Answer(models.Model):
    text = models.TextField(verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False,
                                     verbose_name='Верный ответ')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 verbose_name='Вопрос')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Ответы'
        verbose_name = 'ответ'
        ordering = ('question',)


class Result(models.Model):
    count_questions = models.IntegerField(verbose_name='Количество ответов')
    count_correct_questions = models.IntegerField(
        verbose_name='Количество верных ответов')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True,
                             verbose_name='Пользователь')
    test = models.ForeignKey(Test, on_delete=models.CASCADE,
                             verbose_name='Тест')
    attempt = models.IntegerField(verbose_name='Попытка')

    def __str__(self):
        return f'{self.id}) {self.user} - {self.count_correct_questions}\
            /{self.count_questions}'

    class Meta:
        verbose_name_plural = 'Резуьтаты'
        verbose_name = 'результат'
