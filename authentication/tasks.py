from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

@shared_task
def send_verificacion_email_task(email, code):
    subject = 'Verifica tu cuenta'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [email]

    # Texto plano como fallback
    text_content = f'Tu código de verificación es: {code}'

    # HTML súper básico, compatible con Gmail
    html_content = f"""
    <html>
      <body>
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td align="center">
              <table width="400" cellpadding="20" cellspacing="0" border="0" style="background-color:#ffffff; border:1px solid #ddd;">
                <tr>
                  <td align="center">
                    <h2>¡Bienvenido!</h2>
                    <p>Gracias por registrarte. Tu código de verificación es:</p>
                    <table cellpadding="10" cellspacing="0" border="0" align="center" style="background-color:#007bff; color:#ffffff;">
                      <tr>
                        <td align="center" style="font-size:20px; font-weight:bold;">
                          {code}
                        </td>
                      </tr>
                    </table>
                    <p style="font-size:12px; color:#555;">Si no solicitaste este correo, ignóralo.</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
