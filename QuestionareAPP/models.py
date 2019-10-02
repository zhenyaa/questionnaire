from django.db import models
from CustomUser.models import CustomUser

class Testing(models.Model): #Шапка теста
    nameTest = models.TextField()
    dateQT = models.DateField(auto_now_add=True, blank=True)
    description = models.TextField()
    autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='autor_set', blank=True, null=True, default=None)

    def __repr__(self):
        return self.nameTest

    def __str__(self):
        return self.nameTest

class Question(models.Model): #Вопросы
    deskriptionQuest = models.TextField()

    testing = models.ForeignKey(Testing, on_delete=models.CASCADE)

    def __repr__(self):
        return self.deskriptionQuest
    def __str__(self):
        return self.deskriptionQuest

class Answers(models.Model): #Ответы
    answer = models.TextField()
    itTrue = models.BooleanField()

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __repr__(self):
        return self.answer
    def __str__(self):
        return self.answer

class ResultHead(models.Model): #Шапка ответов на тест
    complited = models.BooleanField(default=False)
    quantTA = models.IntegerField(default=1)
    persentTA = models.FloatField(default=1)

    testingR = models.ForeignKey(Testing, on_delete=models.CASCADE)
    userR = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __setattr__(self, name, value):
        if name == 'quantTA':
            value =  value
        super(ResultHead, self).__setattr__(name, value)


    def setquant(self):
        return self.result_set.filter(trueAnswer = True).count()
    def getAllQuantQuest(self):
        test = self.testingR
        return test.question_set.count()


class Result(models.Model): #Результаты ответов на вопросы
    trueAnswer = models.BooleanField(default=False)
    resultHead = models.ForeignKey(ResultHead, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)




class Comments(models.Model): #Коментарии
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)

    autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    testing = models.ForeignKey(Testing, on_delete=models.CASCADE)







