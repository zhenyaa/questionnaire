from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import ContextMixin
from django.shortcuts import get_list_or_404
from django.db.models import Q
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse_lazy
from .forms import  NewTestFormFactory
from django.forms import formset_factory, inlineformset_factory
from .models import Testing, Question, Answers,CustomUser, ResultHead, Result, Comments
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
#########################################################
from rest_framework import viewsets


class CreateQuestionnareView(CreateView): #создание теста, описание название
    model = Testing
    fields = ['nameTest', 'description']
    template_name = "questionnare/newTest.html"

    def get_success_url(self, **kwargs):
        if kwargs != None:
            return reverse_lazy('CreateQuestion', kwargs = {'pk': self.object.pk})
        else:
            return reverse_lazy('CreateQuestion', args = (self.object.id,))

    def form_valid(self, form):
        form.instance.autor_id = self.request.user.id
        return super(CreateQuestionnareView, self).form_valid(form)


class QuestionAnswerCreateView(View): # создание вопросов ответов
    form_class = NewTestFormFactory
    template_name = 'questionnare/new-questions.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {"myformset": form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        recive_form = NewTestFormFactory(request.POST)
        print('its pk', self.kwargs['pk'])
        if recive_form.is_valid():
            for form in recive_form:
                form.save(self.kwargs["pk"])
            return redirect('home')
        return render(request, self.template_name, {"myformset": recive_form})

class QuestionnareListView(ListView): #список тестов
    model = Testing
    template_name = 'questionnare/test-list.html'

    def get_queryset(self):
        query_set = Testing.objects.order_by("dateQT")
        if self.request.GET.get('filter_name', None):
            query_set = query_set.filter(nameTest__contains= self.request.GET.get('filter_name'))
        if self.request.GET.get('finished', None):
            query_set = query_set.filter(resulthead__userR= self.request.user)
        if self.request.GET.get('notfinished', None):
            query_set = query_set.filter(~Q(resulthead__userR=self.request.user))
        if self.request.GET.get('orderby', None):
            if self.request.GET.get('orderby') == '+ дата созда-я':
                query_set = query_set.order_by('dateQT')
            else: query_set = query_set.order_by('-dateQT')

        return query_set

    def get_context_data(self, **kwargs):
        context = super(QuestionnareListView, self).get_context_data(**kwargs)
        context['filter_name'] = self.request.GET.get('filter_name', '')
        context['orderby'] = self.request.GET.get('orderby')
        context['notfinished'] = self.request.GET.get('notfinished')
        context['finished'] = self.request.GET.get('finished')
        return context

class DeliteTest(DeleteView):
    model = Testing
    success_url = reverse_lazy('ListTestsView')

class DetailQuestionnareView(LoginRequiredMixin,DetailView):#информация об анкете
    model = Testing
    template_name = 'questionnare/detail-test.html'

    def get_context_data(self, **kwargs):
        context = super(DetailQuestionnareView, self).get_context_data(**kwargs)
        context['autor'] = self.get_object().autor
        context['quest'] = get_list_or_404(Question.objects.filter(testing=self.get_object()).order_by("pk"))
        context['addparam'] = context['quest'][0].id
        context['comments'] = Comments.objects.filter(testing=self.get_object())
        context['quant'] = ResultHead.objects.filter(testingR = self.get_object()).count()
        return context

    def post(self, request, *args, **kwargs):
        print(self.request.POST.get('comment'))
        if self.request.POST.get('comment') is not None:
            comment = Comments(comment=self.request.POST.get('comment'), autor = self.request.user, testing =Testing.objects.get(id = self.kwargs['pk']))
            comment.save()
        self.object = self.get_object()
        context = super(DetailQuestionnareView, self).get_context_data(**kwargs)
        context['autor'] = self.get_object().autor
        context['quest'] = get_list_or_404(Question.objects.filter(testing=self.get_object()).order_by("pk"))
        context['addparam'] = context['quest'][0].id
        context['comments'] = Comments.objects.filter(testing=self.get_object())
        return self.render_to_response(context=context)

class StartTest(View,ContextMixin):#пройти тест
    template_name = 'questionnare/start-test.html'
    def get(self, request, *args, **kwargs):
        answers = list()
        questions = Question.objects.filter(testing=self.kwargs['pk'])
        for quest in questions:
            answers.append(quest.answers_set.order_by('?'))
        zip_list = zip(questions,answers )
        return render(request, self.template_name, {"alllist": zip_list})

    def post(self, request, *args, **kwargs ):
        testinnings = Testing.objects.get(pk = self.kwargs['pk'])
        questionnaireResultHead = ResultHead(testingR=testinnings, userR=request.user)
        questionnaireResultHead.save()
        print(request.POST)

        for answer in self.request.POST:
            if answer =='csrfmiddlewaretoken':
                continue
            print(answer,self.request.POST.get(answer) )
            answ = Answers.objects.filter(pk=int(self.request.POST.get(answer))).first()
            print(answ)
            c = Result(resultHead=questionnaireResultHead, answer=answ, trueAnswer=answ.itTrue)
            c.save()
            print('its setquant', questionnaireResultHead.setquant())
            questionnaireResultHead.quantTA = questionnaireResultHead.setquant()
            questionnaireResultHead.save()
            questionnaireResultHead.getAllQuantQuest()
            questionnaireResultHead.persentTA = questionnaireResultHead.quantTA * 100 / questionnaireResultHead.getAllQuantQuest()
            questionnaireResultHead.save()
        return redirect('DetailResultUser', pk = questionnaireResultHead.id)

class DetailResultView(DetailView):#результат теста
    model = ResultHead
    template_name = 'questionnare/detail-result.html'

    def get_context_data(self, **kwargs):
        context = super(DetailResultView, self).get_context_data(**kwargs)
        context['autor'] = self.get_object()
        return context



from .serializers import TestingListSerialize
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Testing.objects.all().order_by('-dateQT')
    serializer_class = TestingListSerialize

from .serializers import StartTestSerialize
class TestingListSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class =  StartTestSerialize