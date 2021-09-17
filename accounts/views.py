from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.core.signing import BadSignature
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import AccountRegistrationForm, AccountUpdateForm
from .utils import signer


# Create your views here.
class AccountRegistrationView(CreateView):
    model = get_user_model()
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('accounts:registration_done')
    form_class = AccountRegistrationForm


class AccountRegistrationDoneView(TemplateView):
    template_name = 'accounts/registration_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'accounts/bad_signature.html')

    user = get_object_or_404(get_user_model(), username=username)
    if user.is_activated:
        template = 'accounts/user_is_activated.html'
    else:
        template = 'accounts/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()

    return render(request, template)


class AccountLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_redirect_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return reverse('index')


class AccountLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


def account_profile_view(request):
    return render(request, 'accounts/profile.html')


class AccountUpdateProfileView(UpdateView):
    model = get_user_model()
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = AccountUpdateForm

    def get_object(self, queryset=None):
        return self.request.user
