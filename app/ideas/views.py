from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms import modelformset_factory
from .models import Idea,IdeaResponse
from questions.models import Category, Question
from django.views.generic.edit import FormView
from django import forms
from django.urls import reverse_lazy
from django.db.models import Q

class IdeaListView(LoginRequiredMixin,ListView):
    model = Idea
    template_name = 'ideas/idea_list.html'
    context_object_name = 'ideas'

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'EVALUATOR']:
            return Idea.objects.filter(Q(user=user) | ~Q(status='incomplete'))
        elif user.role == 'CLIENT':
            return Idea.objects.filter(user=user)
        return Idea.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin_or_evaluator'] = self.request.user.role in ['ADMIN', 'EVALUATOR']
        return context

class IdeaCreateView(LoginRequiredMixin, CreateView):
    model = Idea
    template_name = 'ideas/idea_form.html'
    fields = ['title']

    # def dispatch(self, request, *args, **kwargs):
    #     """Restricción de acceso: Solo usuarios con rol ENTREPRENEUR pueden crear ideas."""
    #     if request.user.role != 'ENTREPRENEUR':
    #         return HttpResponseForbidden("No tienes permiso para crear ideas.")
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtrar categorías y preguntas sin usar `self.object`
        categories = Category.objects.prefetch_related('questions').distinct()
        
        for category in categories:
            for question in category.questions.all():
                if question.type == 'dropdown' and question.options:
                    question.options_list = question.options.split(',')

        context['categories'] = categories
        return context


    def form_valid(self, form):
        """Guarda la idea y verifica si todas las preguntas tienen respuestas."""
        form.instance.user = self.request.user
        self.object = form.save()

        response_data = self.request.POST
        all_questions_answered = True  # Bandera para verificar si todas las preguntas están respondidas

        for key, value in response_data.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]

                # Verifica si la respuesta está vacía
                if not value.strip():
                    all_questions_answered = False
                else:
                    # Guarda la respuesta en el modelo IdeaResponse
                    IdeaResponse.objects.create(
                        idea=self.object,
                        question_id=question_id,
                        answer=value.strip()
                    )

        # Actualiza el estado de la idea
        self.object.status = 'pending' if all_questions_answered else 'incomplete'
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        """Redirige al listado de ideas después de guardar."""
        return reverse('ideas:list')
    
class IdeaEvaluationForm(LoginRequiredMixin, forms.ModelForm):
    observation = forms.CharField(widget=forms.Textarea, label="Observación", required=True)
    note = forms.DecimalField(
        max_digits=4, 
        decimal_places=1, 
        label="Nota", 
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control w-25', 
            'placeholder': 'Ej: 7.0'
        })
    )

    class Meta:
        model = Idea
        fields = ['observation', 'note']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observation'].widget.attrs.update({
            'class': 'form-control',  # Clase de Bootstrap
            'placeholder': 'Escribe tu observación aquí...',  # Placeholder
            'rows': 2,  # Ajusta la altura del textarea
        })

class IdeaDetailView(LoginRequiredMixin,DetailView, FormView):
    model = Idea
    template_name = 'ideas/idea_detail.html'
    context_object_name = 'idea'
    form_class = IdeaEvaluationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        idea_created_at = self.object.created_at

        # Filtrar categorías y preguntas creadas antes o al mismo tiempo que la idea
        categories = Category.objects.prefetch_related(
            'questions'
        ).filter(
            questions__created_at__lte=idea_created_at
        ).distinct()

        responses = {response.question_id: response.answer for response in self.object.responses.all()}

        # Procesar categorías y asociar respuestas
        for category in categories:
            for question in category.questions.all():
                question.answer = responses.get(question.id, 'No respondida')

        context['categories'] = categories

        if self.request.user.role in ['ADMIN', 'EVALUATOR']:
            context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        """Permitir a administradores/evaluadores aprobar o rechazar con observaciones."""
        idea = self.get_object()
        if request.user.role not in ['ADMIN', 'EVALUATOR']:
            return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

        form = self.get_form()
        if form.is_valid():
            observation = form.cleaned_data['observation']
            note = form.cleaned_data['note']
            status = request.POST.get('action', 'pending')
            idea.observation = observation
            idea.status = status
            idea.note = note
            idea.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('ideas:list')

class IdeaUpdateView(LoginRequiredMixin,UpdateView):
    model = Idea
    template_name = 'ideas/idea_form.html'
    fields = ['title']

    def dispatch(self, request, *args, **kwargs):
        """Restricción: Solo el creador puede editar ideas incompletas."""
        idea = self.get_object()
        if idea.user != request.user or idea.status not in ['incomplete', 'rejected']:
            return HttpResponseForbidden("No tienes permiso para editar esta idea.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        idea_created_at = self.object.created_at

        categories = Category.objects.prefetch_related(
            'questions'
        ).filter(
            questions__created_at__lte=idea_created_at
        ).distinct()

        responses = {response.question_id: response.answer for response in self.object.responses.all()}

        for category in categories:
            for question in category.questions.all():
                if question.type == 'dropdown' and question.options:
                    question.options_list = question.options.split(',')
                question.current_answer = responses.get(question.id, '')

        context['categories'] = categories
        return context


    def form_valid(self, form):
        """Guarda la idea y actualiza las respuestas."""
        self.object = form.save()

        response_data = self.request.POST
        all_questions_answered = True

        # Eliminar respuestas existentes para actualizarlas
        IdeaResponse.objects.filter(idea=self.object).delete()

        for key, value in response_data.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]

                if not value.strip():  # Respuesta vacía
                    all_questions_answered = False
                else:
                    IdeaResponse.objects.create(
                        idea=self.object,
                        question_id=question_id,
                        answer=value.strip()
                    )

        # Actualizar estado según las respuestas
        self.object.status = 'pending' if all_questions_answered else 'incomplete'
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        """Redirige al listado de ideas tras la edición."""
        return reverse('ideas:list')

class IdeaDeleteView(LoginRequiredMixin, DeleteView):
    model = Idea
    template_name = 'ideas/idea_confirm_delete.html'
    success_url = reverse_lazy('ideas:list')