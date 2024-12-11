from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AutoRegisterForm, CustomUserUpdateForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def form_invalid(self, form):
        # Puedes imprimir los errores si estás depurando
        print(form.non_field_errors())
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class RegisterView(CreateView):
    form_class = AutoRegisterForm
    template_name = 'users/user_form_plain.html'
    success_url = reverse_lazy('login')

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['users/user_form.html']  # Extiende 'base.html'
        return ['users/user_form_plain.html']  # Extiende 'base_plain.html'

    def form_valid(self, form):
        form.instance.role = 'CLIENT'  # Asignar rol predeterminado
        return super().form_valid(form)

@login_required
class UserListView(UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.role == 'ADMIN'

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        role = self.request.GET.get('role')
        if role:
            queryset = queryset.filter(role=role)
        return queryset
    
@login_required
class UserCreateView(UserPassesTestMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')

    def test_func(self):
        return self.request.user.role == 'ADMIN'
    
    def form_invalid(self, form):
        print(form.errors)  # Depurar errores del formulario
        return super().form_invalid(form)
    
@login_required
class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')

    def test_func(self):
        return self.request.user.role == 'ADMIN'
    
    def form_invalid(self, form):
        # Puedes imprimir los errores si estás depurando
        print(form.non_field_errors())
        return super().form_invalid(form)

@login_required
class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')

    def test_func(self):
        return self.request.user.role == 'ADMIN'
