from urllib.parse import urlparse, urljoin

from celery import shared_task
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http.request import validate_host
from django.template.loader import render_to_string
from django.urls import reverse

from users.models import PasswordResetTokenModel, UserModel


def check_next_url(next_url: str, password_reset_token: PasswordResetTokenModel) -> str:
    if next_url and validate_host(urlparse(next_url).netloc, settings.ALLOWED_HOSTS):
        return urljoin(next_url, password_reset_token.token.__str__())
    return Site.objects.get_current().domain + reverse(
        "users:password_reset_complete", kwargs={"token": password_reset_token.token}
    )


@shared_task
def send_password_reset_email(email_to: str, next_url: str):
    try:
        password_reset_token = PasswordResetTokenModel.objects.get(user__email=email_to)
        user = password_reset_token.user
        url = check_next_url(next_url, password_reset_token)
        context = {"username": user.username, "expired": password_reset_token.expired, "url": url}
        subject = "Сброс пароля"
        html_message = render_to_string("users/email_templates/password_reset.html", context)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = (email_to,)
        send_mail(subject, "", from_email, recipient_list, html_message=html_message)
        print(f"Отправлен email на {user.email}")

    except UserModel.DoesNotExist:
        print(f"Не найден пользователь с таким email: {email_to}")
