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

def bookingConfirmationEmail(email,booking):
    subject= "Booking Confirmation - HostStay"
    message= f"""Hi {booking.guest.first_name},

Your reservation has been successfully confirmed.

Booking Details:
Property: {booking.hotel.hotel_name}
Check-in: {booking.check_in}
Check-out: {booking.check_out}
Guests: {booking.guests}
Booking ID: {booking.id}

We look forward to hosting you and hope you have a wonderful stay.

Thank you for choosing HostStay.

Regards,
HostStay Team
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    
def hostBookingCancellationEmail(host_email, booking):

    subject = "Guest Reservation Cancelled - HostStay"

    message = f"""Hello Host,

A guest has cancelled an existing reservation for your property.

Cancelled Reservation Details:

Property: {booking.hotel.hotel_name}
Guest: {booking.guest.get_full_name() or booking.guest.username}
Guest Email: {booking.guest.email}

Check-in: {booking.check_in}
Check-out: {booking.check_out}
Guests: {booking.guests}

Booking ID: {booking.id}

The dates covered by this reservation are now available for new bookings.

Regards,
HostStay Team
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [host_email],
        fail_silently=False,
    )

def userbookingCancellationEmail(guest_email, booking):

    subject = "Reservation Cancelled - HostStay"

    message = f"""Hi {booking.guest.first_name},

Your reservation has been cancelled successfully.

Cancelled Booking Details:
Property: {booking.hotel.hotel_name}
Check-in: {booking.check_in}
Check-out: {booking.check_out}
Guests: {booking.guests}
Booking ID: {booking.id}

The dates for this reservation have now been released and made available for booking again.

If this cancellation was made by mistake, you can make a new reservation through HostStay.

Thank you for choosing HostStay.

Regards,
HostStay Team
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [guest_email],
        fail_silently=False,
    )