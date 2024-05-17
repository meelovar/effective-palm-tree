from django.contrib.auth import mixins
from django.contrib.auth import views as auth_views
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from apps.users import utils
from apps.users.forms import (
    PasswordResetForm,
    RegistrationForm,
)
from apps.users.models import User


class CheckTokenMixin:
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            error_message = "The URL path must contain 'uidb64' and 'token' parameters."

            raise ImproperlyConfigured(error_message)
        try:
            uid = urlsafe_base64_decode(kwargs["uidb64"]).decode()
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            self.user = None

        if self.user is not None:
            if default_token_generator.check_token(self.user, kwargs["token"]):
                self.validlink = True
            else:
                self.validlink = False
        else:
            self.validlink = False

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["validlink"] = self.validlink

        return context


class RegisterView(generic.CreateView):
    template_name = "users/register.html"
    success_url = reverse_lazy("register_done")
    form_class = RegistrationForm

    def form_valid(self, form):
        user = form.save(commit=False)

        user.is_active = False

        user.save()

        self.object = user
        self.request.user = user

        utils.send_email(self.request, False, "Confirm registration", "users/registration_confirm_email.html")

        return HttpResponseRedirect(self.get_success_url())


class RegisterDoneView(generic.TemplateView):
    template_name = "users/register_done.html"


class RegisterConfirmView(CheckTokenMixin, generic.TemplateView):
    template_name = "users/register_confirm.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        self.user.is_active = True

        self.user.save()

        return self.render_to_response(context)


class UserListView(generic.ListView):
    model = User
    ordering = "date_joined"


class UserDetailView(generic.DetailView):
    model = User
    context_object_name = "u"


class UserEditView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ("first_name", "last_name")
    success_url = reverse_lazy("user_change")

    def get_object(self, queryset=None):
        return self.request.user


class EmailResetView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = "users/email_reset.html"

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)

        utils.send_email(request, False, "Reset email", "users/email_reset_email.html")

        return result


class EmailResetConfirmView(CheckTokenMixin, generic.UpdateView):
    model = User
    fields = ("email",)
    template_name = "users/email_reset_confirm.html"

    def get_object(self, queryset=None):
        return self.user


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = "users/password_change_form.html"


class PasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetForm
    template_name = "users/password_reset_form.html"


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "users/password_reset_complete.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
