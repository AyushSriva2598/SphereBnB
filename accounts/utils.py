import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import Hotel


def generateRandomToken():
    return str(uuid.uuid4())

def sendEmailToken(email, token):
    subject= "Verify Your Email Address"
    message= f"""Hi Pls verify your email account by clicking this link
    http://127.0.0.1:8000/accounts/verify-account/{token}/
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def sendOTPtoEmail(email, otp):
    subject= "OTP for login"
    message= f"""Hi This is OTP for account login
    {otp}
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def sendEmailTokenHost(email, token):
    subject= "Verify Your Email Address"
    message= f"""Hi Pls verify your host email account by clicking this link
    http://127.0.0.1:8000/accounts/verify-account-host/{token}/
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def sendOTPtoEmailHost(email, otp):
    subject= "OTP for login"
    message= f"""Hi This is OTP for host account login
    {otp}
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def generateSlug(hotel_name):
    slug= slugify(hotel_name) + "-" + str(uuid.uuid4()).split('-')[0]
    if Hotel.objects.filter(hotel_slug=slug).exists():
        return generateSlug(hotel_name)
    
    return slug
    
    