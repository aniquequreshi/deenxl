from django.contrib import admin

# Register your models here.
from .models import Question, Subject, Level, ChoiceGroup, Choice

admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(Level)
admin.site.register(ChoiceGroup)
admin.site.register(Choice)