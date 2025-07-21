import random
from django.utils import timezone
from .models import UserVerificationCode
from .tasks import send_verificacion_email_task


def generate_code():
    return str(random.randint(100000, 999999))


def send_verification_email(user):
    code = generate_code()
    UserVerificationCode.objects.create(user=user, code=code)

    send_verificacion_email_task.delay(user.email, code)


def verify_code(user, code_input):
    try:
        record = UserVerificationCode.objects.filter(user=user, code=code_input, is_used=False).latest('created_at')
        if record.is_expired():
            return False, "Codigo expirado"
        record.is_used = True
        record.save()
        return True, "Codigo valido"
    except UserVerificationCode.DoesNotExist:
        return False, "Código no válido"