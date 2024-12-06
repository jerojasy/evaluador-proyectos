from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name
class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Texto Libre'),
        ('number', 'Número'),
        ('dropdown', 'Opciones Desplegables'),
    ]

    text = models.CharField(max_length=255, verbose_name="Texto de la Pregunta")
    type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name="Tipo de Respuesta")
    options = models.TextField(blank=True, null=True, verbose_name="Opciones (separadas por comas)")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden de la Pregunta")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="questions", verbose_name="Categoría", null=True, blank=True)


    class Meta:
        ordering = ['category','order']

    def __str__(self):
        return self.text
