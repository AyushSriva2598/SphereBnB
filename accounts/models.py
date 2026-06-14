from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class HotelUser(User):
    profile_picture = models.ImageField(upload_to="profile")
    phone_number = models.CharField(unique=True, max_length=100)
    email_token= models.CharField(max_length=100,null=True, blank=True)
    otp= models.CharField(max_length=10, null=True, blank=True)
    is_verified= models.BooleanField(default=False)
    
    class Meta:
        db_table="hotel_users"


class HotelVendor(User):
    profile_picture = models.ImageField(upload_to="profile")
    phone_number = models.CharField(unique=True)
    business_name=models.CharField(max_length=100)
    email_token= models.CharField(max_length=100,null=True, blank=True)
    otp= models.CharField(max_length=10, null=True, blank=True)
    is_verified= models.BooleanField(default=False)

    class Meta:
        db_table="hotel_hosts"


class Ameneties(models.Model):
    name=models.CharField(max_length=100)
    icon=models.ImageField(upload_to="hotels")

    def __str__(self) -> str:
        return self.name


class Hotel(models.Model):
    hotel_name= models.CharField(max_length=100)
    hotel_description=models.TextField()
    hotel_slug= models.SlugField(max_length=1000,unique=True)
    hotel_owner=models.ForeignKey(HotelVendor,on_delete=models.CASCADE, related_name="hotel_owner")
    ameneties= models.ManyToManyField(Ameneties)
    hotel_price=models.FloatField()
    hotel_offer_price=models.FloatField()
    hotel_location=models.TextField()
    is_active=models.BooleanField(default=True)

class HotelImage(models.Model):
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE, related_name="hotel_images")
    image=models.ImageField(upload_to="hotels")

class HotelManager(models.Model):
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE, related_name="hotel_manager")
    manager_name=models.CharField(max_length=100)
    manager_contact=models.CharField(max_length=100)


class Booking(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="bookings")
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")

    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.hotel_name} | {self.check_in} → {self.check_out} ({self.guest})"