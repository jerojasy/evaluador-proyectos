"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.views import CustomLoginView, CustomLogoutView, RegisterView, UserListView, UserCreateView, UserUpdateView, UserDeleteView
from .views import home



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    # users
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='user-edit'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    # mantenedor preguntas
    path('questions/', include('questions.urls')),
    # ideas
    path('ideas/', include('ideas.urls', namespace='ideas')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)