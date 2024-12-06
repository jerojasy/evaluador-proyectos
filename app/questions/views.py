from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Question, Category

class QuestionListView(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'grouped_questions'

    def get_queryset(self):
        return Question.objects.select_related('category').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped_questions = {}
        for question in self.get_queryset():
            grouped_questions.setdefault(question.category, []).append(question)
        context['grouped_questions'] = grouped_questions
        return context


class QuestionCreateView(CreateView):
    model = Question
    fields = ['text', 'type', 'options', 'order', 'category']
    template_name = 'questions/question_form.html'
    success_url = reverse_lazy('questions:list')


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['text', 'type', 'options', 'order', 'category']
    template_name = 'questions/question_form.html'
    success_url = reverse_lazy('questions:list')


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'questions/question_confirm_delete.html'
    success_url = reverse_lazy('questions:list')
