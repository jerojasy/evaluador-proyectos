from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Question
from .forms import QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin


class QuestionListView(LoginRequiredMixin,ListView):
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
    try:
        from .forms import QuestionForm
        print("Formulario importado correctamente")
    except ImportError as e:
        print(f"Error importando QuestionForm: {e}")

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    # fields = ['text', 'type', 'options', 'order', 'category']
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    success_url = reverse_lazy('questions:list')


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    # fields = ['text', 'type', 'options', 'order', 'category']
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    success_url = reverse_lazy('questions:list')

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'questions/question_confirm_delete.html'
    success_url = reverse_lazy('questions:list')
