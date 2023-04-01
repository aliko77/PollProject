from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.contrib import messages
from django.views.generic import UpdateView
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str

from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

from .models import Profile, User
from .utils import account_activate_token


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
        if request.user.is_authenticated:
            return redirect('home')
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            SendVerificationEmail(request, user)
            messages.success(
                request=request, message='Başarıyla kayıt oldunuz. Lütfen mail adresinizi doğrulayınız.'
            )
            return redirect('login')
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


class SendVerificationEmail:
    def __init__(self, request, user):
        self.request = request
        self.send(user)

    def send(self, user):
        mail_subject = 'Mail Doğrulama.'
        current_site = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activate_token.make_token(user)
        message = render_to_string('account/activate_account.html', {
            'user': user, 'domain': current_site.domain,
            'uid' : uid, 'token': token
        }
        )
        email = send_mail(mail_subject, message, settings.EMAIL_HOST_USER, (user.email,),
            fail_silently=True
        )
        return True if email else False


class ActivateView(View):
    @staticmethod
    def get(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, TypeError, ValueError, OverflowError):
            user = None
        if user is not None and not user.is_active and account_activate_token.check_token(user=user, token=token):
            user.is_active = True
            user.save()
            login(request=request, user=user)
            messages.info(request, 'Hesabın başarıyla doğrulandı.')
            return redirect('home')
        else:
            messages.error(request, 'Bilinmeyen istek.')
            return redirect('home')
