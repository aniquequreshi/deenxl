from django.urls import path

from . import views
from .views import ChoiceCreateView

app_name = 'questions'
urlpatterns = [
    path('ajax/load-choices/', views.load_choices, name='ajax_load_choices'),

    path('create/', views.QuestionCreateView.as_view(), name='question-create'),
    path('update/<int:pk>/', views.QuestionUpdateView.as_view(), name='question-update'),
    path('list/', views.QuestionListView.as_view(), name='question-list'),
    # path('detail/<int:pk>/', views.DetailView.as_view(), name='question-detail'),
    # path('delete/<int:pk>/', views.DeleteView.as_view(), name='question-delete'),

    path('choice/group/create/', views.ChoiceGroupCreateView.as_view(), name='choice-group-create'),
    path('choice/group/update/<int:pk>/', views.ChoiceGroupUpdateView.as_view(), name='choice-group-update'),
    # path('choice/group/list/', views.ChoiceGroupListView.as_view(), name='choice-group-list'),
    # path('choice/group/detail/<int:pk>/', views.ChoiceGroupDetailView.as_view(), name='choice-group-detail'),
    # path('choice/group/delete/<int:pk>/', views.ChoiceGroupDeleteView.as_view(), name='choice-group-delete'),

    path('choice/create/<int:pk>/', ChoiceCreateView, name='choice-create'),
    # path('choice/update/<int:pk>/', views.ChoiceUpdateView.as_view(), name='choice-update'),
    # path('choice/list/', views.ChoiceListView.as_view(), name='choice-list'),
    # path('choice/detail/<int:pk>/', views.ChoiceDetailView.as_view(), name='choice-detail'),
    # path('choice/delete/<int:pk>/', views.ChoiceDeleteView.as_view(), name='choice-delete'),

    path('copy/<int:pk>/', views.QuestionCopy, name='question-copy'),
    path('generate/<int:pk>/', views.QuestionGenerate, name='question-generate'),
    path('answer/check/<int:pk>/', views.questionCheckAnswer, name='question-answer-check'),
    # path('answer/display/', views.questionAnswerDisplay, name='question-answer-display'),
]