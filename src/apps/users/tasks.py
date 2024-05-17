import dramatiq
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template import loader


@dramatiq.actor
def send_email_reset_email(subject, email_template_name, context):
    body = loader.render_to_string(email_template_name, context)

    send_mail(subject, body, None, [context["email"]])


@dramatiq.actor
def send_password_reset_email(
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
):
    subject = loader.render_to_string(subject_template_name, context)
    subject = "".join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")

    email_message.send()
