from django.contrib.auth.models import User, Group
from .models import Question, Testing
from rest_framework import serializers

class TestingListSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Testing
        fields = ['url', 'nameTest', 'dateQT', 'description']




# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']