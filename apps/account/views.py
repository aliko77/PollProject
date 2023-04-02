from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib import messages
from django.views.generic import UpdateView
from django.utils.encoding import force_str

from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

from .models import Profile, User
from .utils import account_activate_token, SendVerificationEmail


# Create your views here.


class Login(LoginView):
    template_name = "account/login.html"
    redirect_field_name = "next"

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_verified:
                login(self.request, user)
                return super().form_valid(form)
            else:
                return redirect("account.verify", email=user.email)

    def form_invalid(self, form):
        messages.error(self.request, 'Email veya şifre yanlış')
        return self.render_to_response(self.get_context_data(form=form))


class Register(View):
    template_name = "account/register.html"

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            SendVerificationEmail(request, user)
            return redirect('account.verify', email=user.email)
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request):
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


class AccountVerify(View):
    template_name = "account/verify-information.html"

    def get(self, request, email):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            try:
                User.objects.get(email=email, is_verified=False)
            except User.DoesNotExist:
                return redirect("home")
        return render(request, self.template_name, {"email": email})


class ActivateView(View):
    @staticmethod
    def get(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, TypeError, ValueError, OverflowError):
            user = None
        if user is not None and \
                user.is_verified is False and \
                account_activate_token.check_token(user=user, token=token):
            user.is_verified = True
            user.save()
            login(request=request, user=user)
            messages.info(request, 'Hesabın başarıyla doğrulandı.')
            return redirect('home')
        else:
            messages.error(request, 'Bilinmeyen istek.')
            return redirect('home')
