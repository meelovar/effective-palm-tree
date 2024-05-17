from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.users.tasks import send_email_reset_email


def send_email(request, use_https, subject, email_template_name):
    current_site = get_current_site(request)
    domain = current_site.domain
    user = request.user
    context = {
        "domain": domain,
        "email": user.email,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user),
        "protocol": "https" if use_https else "http",
    }

    send_email_reset_email.send(subject, email_template_name, context)
