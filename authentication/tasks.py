from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_verificacion_email_task(email, code):
    subject = 'Código de verificación'
    message = f'Tu código de verificación es: {code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)