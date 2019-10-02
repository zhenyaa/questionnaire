from django.contrib import admin
from .models import Question, Testing, Answers
admin.site.register(Testing)
admin.site.register(Question)
admin.site.register(Answers)
# Register your models here.
