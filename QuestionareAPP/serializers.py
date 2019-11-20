from django.contrib.auth.models import User, Group
from .models import Question, Testing, Answers
from rest_framework import serializers

class TestingListSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Testing
        fields = ['url', 'nameTest', 'dateQT', 'description']





class AnswersListSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answers
        fields = ['answer', 'itTrue']


class StartTestSerialize(serializers.HyperlinkedModelSerializer):
    answer = AnswersListSerialize(many=True)
    class Meta:
        model = Question
        fields = ['url', 'deskriptionQuest', 'answer' ]

class DetailTestSerialize(serializers.HyperlinkedModelSerializer):
    questions = StartTestSerialize(many=True)

    class Meta:
        model = Testing
        fields = ['url', 'nameTest', 'dateQT', 'description', 'questions']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']