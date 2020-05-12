from django.conf import settings
from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Create your models here.

class ChoiceGroup(models.Model):
    choice_group = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                   editable=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_modified']

    def get_absolute_url(self):
        return reverse('questions:choice-group-create', kwargs={'pk': self.pk})

    def __str__(self):
        return self.choice_group


class Choice(models.Model):
    choice = models.CharField(max_length=1000)
    choice_group = models.ForeignKey('ChoiceGroup', on_delete=models.PROTECT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                   editable=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_modified']
        unique_together = [['choice', 'choice_group']]

    def __str__(self):
        return self.choice


class Subject(models.Model):
    subject = models.CharField(max_length=100)

    class Meta:
        ordering = ['subject']

    def __str__(self):
        return self.subject


class Level(models.Model):
    level = models.CharField(max_length=2)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.level


class Question(models.Model):
    question_text = models.TextField(verbose_name='Question')
    choice_group = models.ForeignKey('ChoiceGroup', on_delete=models.PROTECT, verbose_name='Choice Group')
    choice = models.ForeignKey('Choice', on_delete=models.PROTECT, verbose_name='Correct Answer')
    notes = models.TextField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    subject = models.ManyToManyField(Subject)
    level = models.ManyToManyField(Level)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                   editable=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # class Meta:
    # verbose_name_plural = "questions_standard"
    class Meta:
        ordering = ['-last_modified']

    def __str__(self):
        return self.question_text
