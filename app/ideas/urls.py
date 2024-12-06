from django.urls import path
from .views import IdeaListView, IdeaCreateView, IdeaDetailView, IdeaUpdateView

app_name = 'ideas'

urlpatterns = [
    path('', IdeaListView.as_view(), name='list'),  # URL para el listado de ideas
    path('create/', IdeaCreateView.as_view(), name='create'),
    path('<int:pk>/', IdeaDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', IdeaUpdateView.as_view(), name='edit'),  # Editar idea

]
