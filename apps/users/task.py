from celery import shared_task
from django.core.mail import send_mail
from root.settings import EMAIL_HOST_USER


@shared_task(bind=True)
def send_verification_email(self, email, code):
    try:
        subject = "Your Verification Code"
        message = f"Your verification code is: {code}"
        from_email = EMAIL_HOST_USER
        recipient_list = [email]

        result = send_mail(subject, message, from_email, recipient_list)
        return {"status": "ok", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
