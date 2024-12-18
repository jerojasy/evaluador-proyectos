from django import forms
from .models import Question
from django_summernote.widgets import SummernoteWidget

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'type', 'options', 'order', 'category']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control w-50',
                'placeholder': 'Ingrese el texto de la pregunta'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select form-control w-50'
            }),
            'options': forms.Textarea(attrs={
                'class': 'form-control w-50',
                'rows': 3,
                'placeholder': 'Ingrese opciones separadas por comas (si aplica)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control w-50',
                'placeholder': 'Orden de la pregunta'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-control w-50'
            }),
        }

class AnswerForm(forms.Form):
    # Agregar campo WYSIWYG solo para respuestas
    wysiwyg_answer = forms.CharField(widget=SummernoteWidget(), required=False)