from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _

from apps.users import tasks
from apps.users.models import User


class RegistrationForm(auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class EmailResetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)


class PasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput({"autocomplete": "email"}))

    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None,
    ):
        context["user"] = str(context["user"].id)

        tasks.send_password_reset_email.send(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None,
        )
