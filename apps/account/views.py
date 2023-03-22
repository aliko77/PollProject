from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import UpdateView

from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

from .models import Profile, User


# Create your views here.


class Login(LoginView):
    template_name = "account/login.html"
    redirect_field_name = "next"

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Email veya şifre yanlış')
        return self.render_to_response(self.get_context_data(form=form))


class Register(View):
    template_name = "account/register.html"

    def post(self, request):
        """
        redirect guest users to home page
        """
        if request.user.is_authenticated:
            return redirect('home')
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request=request, message='Başarıyla kayıt oldunuz.'
            )
            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request):
        """
        redirect guest users to home page
        """
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)


class Logout(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        logout(request=request)
        return redirect('home')


class AccountEdit(LoginRequiredMixin, View):
    template_name = "account/edit.html"

    def get(self, request):
        return render(request, self.template_name)


class AccountDetailUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["name"]
    success_url = reverse_lazy("account.edit")

    def get_object(self, queryset=None):
        return self.request.user


class AccountProfilePhotoUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ["image"]
    success_url = reverse_lazy("account.edit")

    def get_object(self, queryset=None):
        return self.request.user.profile
