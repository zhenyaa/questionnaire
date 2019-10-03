from django import forms
from django.forms import formset_factory, inlineformset_factory, ModelForm
from .models import Answers,Question, ResultHead, Testing

class NewTestForm(forms.Form):
    question = forms.CharField(max_length=100, label='Вопрос')
    answer1 = forms.CharField(label='Верный ответ')
    answer2 = forms.CharField(label='Ответ')
    answer3 = forms.CharField(label='Ответ')
    answer4 = forms.CharField(label='Ответ')

    def save(self, pk):
        question = Question(deskriptionQuest = self.cleaned_data['question'], testing =  Testing.objects.get(pk=pk))
        question.save()
        ans1 = Answers(answer = self.cleaned_data['answer1'], itTrue = True, question = question)
        ans2 = Answers(answer=self.cleaned_data['answer2'], itTrue=False, question=question)
        ans3 = Answers(answer=self.cleaned_data['answer3'], itTrue=False, question=question)
        ans4 = Answers(answer=self.cleaned_data['answer4'], itTrue=False, question=question)

        ans1.save()
        ans2.save()
        ans3.save()
        ans4.save()
        return question

NewTestFormFactory = formset_factory(NewTestForm, extra= 5, min_num=5)



