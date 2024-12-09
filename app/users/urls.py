from django.urls import path
from .views import CustomLoginView, CustomLogoutView, RegisterView, UserListView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='user-edit'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete')
]
