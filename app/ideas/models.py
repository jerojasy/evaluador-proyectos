from django.db import models
from django.conf import settings
from questions.models import Question, Category

class Idea(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente de evaluación'),
        ('rejected', 'Rechazada'),
        ('approved', 'Aprobada'),
        ('incomplete', 'Sin terminar'),
    ]

    title = models.CharField(max_length=255, verbose_name="Título de la Idea")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ideas", verbose_name="Usuario")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incomplete', verbose_name="Estado")
    observation = models.TextField(null=True, blank=True, verbose_name="Observación")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Idea"
        verbose_name_plural = "Ideas"

    def __str__(self):
        return self.title


class IdeaResponse(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="responses", verbose_name="Idea")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Pregunta")
    answer = models.TextField(verbose_name="Respuesta")

    class Meta:
        unique_together = ('idea', 'question')
        verbose_name = "Respuesta de Idea"
        verbose_name_plural = "Respuestas de Ideas"

    def __str__(self):
        return f"{self.idea.title} - {self.question.text}"
