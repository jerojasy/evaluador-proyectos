from django.contrib import admin
from .models import Category, Question

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'type', 'order')
    list_filter = ('category',)
    list_editable = ('order',)
    ordering = ('order', 'category')
