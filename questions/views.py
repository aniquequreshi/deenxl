from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from random import randint, shuffle

from .models import Question, Choice, ChoiceGroup, Subject
from .forms import QuestionForm
# , ChoiceForm
from django.forms import inlineformset_factory

# Delete Questions, then Choices, then Groups
def index_view(request):
    return render(request, 'questions/index.html')


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    # fields = '__all__'
    success_url = reverse_lazy('questions:question-list')

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm

    # fields = ('question_text', 'choice_group', 'choice', 'notes',)
    success_url = reverse_lazy('questions:question-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class QuestionListView(LoginRequiredMixin, ListView):
    model = Question

    def get_queryset(self):
        user = self.request.user
        question_list = Question.objects.filter(created_by=user)
        return question_list

# class QuestionDetailView(LoginRequiredMixin, DetailView):
#     model = Question


# class QuestionDeleteView(LoginRequiredMixin, DeleteView):
#     model = Question
#     success_url = reverse_lazy('questions:question-list')
#
#     def get_queryset(self):
#         user = self.request.user
#         question_list = Question.objects.filter(created_by=user)
#         return question_list

def load_choices(request):
    choice_group_id = request.GET.get('choice_group')
    choices = Choice.objects.filter(choice_group_id=choice_group_id)
    return render(request, 'questions/choice_dropdown_list_options.html', {'choices': choices})


class ChoiceGroupCreateView(LoginRequiredMixin, CreateView):
    model = ChoiceGroup
    # form_class = ChoiceGroupForm
    fields = '__all__'
    # success_url = 'questions:index'
    success_url = reverse_lazy('questions:choice-group-create')

    # form = QuestionForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self.model.objects.filter(created_by=self.request.user)
        return context

class ChoiceGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = ChoiceGroup
    fields = ('choice_group',)
    success_url = reverse_lazy('questions:choice-group-create')

# Works but don't need it
# class ChoiceGroupListView(LoginRequiredMixin, ListView):
#     model = ChoiceGroup
#     # permission_required = ('kidsapp.view_denial')
#     def get_queryset(self):
#         user = self.request.user
#         choice_group_list = ChoiceGroup.objects.filter(created_by=user)
#         return choice_group_list


# class ChoiceGroupDetailView(LoginRequiredMixin, DetailView):
#     model = ChoiceGroup


# class ChoiceGroupDeleteView(LoginRequiredMixin, DeleteView):
#     model = ChoiceGroup
#     success_url = reverse_lazy('author-list')
#
#     def get_queryset(self):
#         user = self.request.user
#         choice_group_list = ChoiceGroup.objects.filter(created_by=user)
#         return choice_group_list


# class ChoiceCreateView(LoginRequiredMixin, CreateView):
#     model = Choice
#     # form_class = ChoiceGroupForm
#     fields = '__all__'
#     # success_url = 'questions:index'
#     success_url = reverse_lazy('questions:choice-list')
#
#     # form = QuestionForm
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)

def ChoiceCreateView(request, pk):
    ChoiceFormSet = inlineformset_factory(ChoiceGroup, Choice, fields=('choice',), extra=5)
    choice_group = ChoiceGroup.objects.get(id=pk)

    if request.method == 'POST':
        formset = ChoiceFormSet(request.POST, instance = choice_group)
        if formset.is_valid():
            formset.save()
            return redirect('questions:choice-create', pk = choice_group.id)

    # IMPORTANT: Change queryset objects.none() to not show older items in list
    # formset = ChoiceFormSet(queryset=Choice.objects.none(),instance=choice_group)
    formset = ChoiceFormSet(queryset=Choice.objects.all(), instance=choice_group)
    context = {'formset': formset, 'choice_group':choice_group}
    return render(request, 'questions/choice_form.html', context)


class ChoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Choice
    fields = ('choice',)
    success_url = reverse_lazy('questions:choice-list')

    # def get_queryset(self):
    #     user = self.request.user
    #     choice_list = Choice.objects.filter(created_by=user)
    #     return choice_list


class ChoiceListView(LoginRequiredMixin, ListView):
    model = Choice


# class ChoiceDetailView(LoginRequiredMixin, DetailView):
#     model = Choice


# class ChoiceDeleteView(LoginRequiredMixin, DeleteView):
#     model = Choice
#     success_url = reverse_lazy('questions:choice-list')

def QuestionCopy(request, pk):
    # form_class = QuestionForm

    question = Question.objects.get(id=pk)
    question.pk = None
    # question.question_text = 'COPY:' + question.question_text
    question.save()
    # new_id = question.id
    # context = {'question':question}

    # if request.method == 'POST':
    #     formset = ChoiceFormSet(request.POST, instance = choice_group)
    #     if formset.is_valid():
    #         formset.save()
    #         return redirect('questions:choice-create', pk = choice_group.id)

    return redirect('questions:question-update', pk = question.id)
    # return render(request, "questions/question_copy.html", context)
    # questions / question_form.html

def QuestionGenerate(request, pk):
    question = Question.objects.get(id=pk)
    choice_group = question.choice_group
    correct_choice = question.choice
    # Below is needed to create a Queryset for combining
    correct_choice_qs = Choice.objects.filter(choice_group = choice_group, choice = correct_choice).order_by("?")[:1]
    wrong_choices = Choice.objects.filter(choice_group = choice_group).exclude(choice = correct_choice).order_by("?")[:4]
    all_choices = correct_choice_qs | wrong_choices

    all_choices_list = list(all_choices)
    shuffle(all_choices_list)

    context = {'question':question, 'all_choices': all_choices_list}
    return render(request, "questions/question_generate.html", context)