from django.urls import path
from . import views
from django.conf.urls import url
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'testing', views.UserViewSet)


urlpatterns = [

    path('createtest/', views.CreateQuestionnareView.as_view(), name='createTest'), #создание теста
    path('createquest/<int:pk>', views.QuestionAnswerCreateView.as_view(), name='CreateQuestion'), #создание вопросов
    path('listquestion', views.QuestionnareListView.as_view(), name='ListTestsView'),# СПИСОК ТЕСТОВ
    path('datailtest/<int:pk>', views.DetailQuestionnareView.as_view(), name='DetailTest'),# детали теста
    path('starttest/<int:pk>', views.StartTest.as_view(), name='StartTest'),# пройти тест
    path('detailresult/<int:pk>', views.DetailResultView.as_view(), name = 'DetailResultUser'),# результат теста
    path('deltest/<int:pk>', views.DeliteTest.as_view(), name='deleteView'),#удалить тест
    # path('addcomment/<int:pk>', views.AddComment.as_view(), name='AddComment')#Добавить комментарий
]
