from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.models import User
from .models import HotelUser, HotelVendor, Hotel, Ameneties, HotelImage
from django.db.models import Q
from .utils import generateRandomToken, sendEmailToken, sendOTPtoEmail, sendEmailTokenHost, sendOTPtoEmailHost,generateSlug
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
import random


# Create your views here.
def login_view(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        hotel_user = HotelUser.objects.filter(email =email)

        if not hotel_user.exists():
            messages.warning(request, "No Account Found")
            return redirect('/account/login/')
        
        
        if not hotel_user[0].is_verified:
            messages.warning(request,"Account not verified")
            return redirect('/account/login/')
        
        hotel_user=authenticate(username=hotel_user[0].username, password=password)

        if hotel_user:
            messages.success(request,"Login Success")
            login(request, hotel_user)
            return redirect('/account/login/')
        
        messages.warning(request,"Invalid Credentials")
        return redirect('/account/login/')



    return render(request,'user/login.html')

def register_view(request):
    if request.method == "POST":
        name= request.POST.get('name')
        email= request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        password=request.POST.get('password')
        confirmPassword=request.POST.get('confirm_password')
        hotel_user=HotelUser.objects.filter(Q(username=name)| Q(phone_number=phone_number))
        if hotel_user.exists():
            messages.success(request,"Username is already taken")
            return redirect('register_view')
        
        
        hotel_user=HotelUser.objects.create(
            username=phone_number,
            first_name=name.split()[0],
            last_name=name.split()[-1],
            email=email,
            phone_number=phone_number,
            email_token=generateRandomToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email,hotel_user.email_token)
        messages.success(request,"An email sent to your Email")
        return redirect('register_view')
    
    return render(request,'user/register.html')



def verify_email_token(request, token):
    try:
        hotel_user=HotelUser.objects.get(email_token=token)
        hotel_user.is_verified=True
        hotel_user.save()
        messages.success(request,"Email Verified")
        return redirect('/accounts/login')
    except Exception as e:
        return HttpResponse("Invalid Token")
    

def send_OTP(request):
    if request.method == "GET":
        return render(request, "user/otp.html")
    
    
    email= request.POST.get('email')
    hotel_user = HotelUser.objects.filter(email =email)

    if not hotel_user.exists():
            messages.warning(request, "No Account Found")
            print(f'No account found')
            return redirect('/accounts/login/')
    otp=random.randint(1000,9999)
    hotel_user.update(otp=otp)
    sendOTPtoEmail(email,otp)

    return render(
        request,
        "user/otp.html",
        {
            "otp_sent": True,
            "email": email
        }
    )
    # return render(request,'register.html')



def verify_otp(request, email):
    if request.method == "POST":
        otp=request.POST.get('otp')
        hotel_user=HotelUser.objects.get(email=email)

        if otp == hotel_user.otp:
            messages.success(request, "Login Success")
            login(request,hotel_user)
            return redirect('/accounts/login')
        
        messages.warning(request,"Wrong OTP")
        return redirect(f'/accounts/verify-otp/{email}/')
    

    return render(request, 'user/otp.html')


def host_login(request):
    if request.method == "POST":
        email=request.POST.get('email')
        print("POST:", request.POST)
        print("EMAIL:", email)

        hotel_host = HotelVendor.objects.filter(
            email__iexact=email.strip()
        )

        print("COUNT:", hotel_host.count())
        password=request.POST.get('password')

        hotel_host = HotelVendor.objects.filter(email =email)

        if not hotel_host.exists():
            messages.warning(request, "No host Account Found")
            return redirect('/accounts/host-login/')
        
        
        if not hotel_host[0].is_verified:
            messages.warning(request,"Account not verified")
            return redirect('/accounts/host-login/')
        
        hotel_host=authenticate(username=hotel_host[0].username, password=password)

        if hotel_host:
            messages.success(request,"Login Success")
            login(request, hotel_host)
            return redirect('/accounts/host-dashboard/')
        
        messages.warning(request,"Invalid Credentials")
        return redirect('/accounts/host-login/')
    return render(request,"host/host_login.html")


def host_register(request):
    if request.method == "POST":
        name= request.POST.get('name')
        email= request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        business_name=request.POST.get('business_name')
        password=request.POST.get('password')
        confirmPassword=request.POST.get('confirm_password')
        hotel_host=HotelVendor.objects.filter(Q(username=name)| Q(phone_number=phone_number))
        if hotel_host.exists():
            messages.success(request,"Username is already taken")
            return redirect('register_view')
        
        
        hotel_host=HotelVendor.objects.create(
            username=phone_number,
            first_name=name.split()[0],
            last_name=name.split()[-1],
            email=email,
            phone_number=phone_number,
            email_token=generateRandomToken()
        )
        hotel_host.set_password(password)
        hotel_host.save()

        sendEmailTokenHost(email,hotel_host.email_token)
        messages.success(request,"An email sent to your Email")
        return redirect('host_register')
    return render(request,"host/host_register.html")

def verify_email_token_host(request, token):
    try:
        hotel_host=HotelVendor.objects.get(email_token=token)
        hotel_host.is_verified=True
        hotel_host.save()
        messages.success(request,"Email Verified")
        return redirect('/accounts/host-login')
    except Exception as e:
        return HttpResponse("Invalid Token")


def send_OTP_host(request):
    if request.method == "GET":
        return render(request, "host/host_otp.html")
    
    
    email= request.POST.get('email')
    hotel_host = HotelVendor.objects.filter(email =email)

    if not hotel_host.exists():
            messages.warning(request, "No Account Found")
            print(f'No account found')
            return redirect('/accounts/login/')
    otp=random.randint(1000,9999)
    hotel_host.update(otp=otp)
    sendOTPtoEmailHost(email,otp)

    return render(
        request,
        "host/host_otp.html",
        {
            "otp_sent": True,
            "email": email
        }
    )
    # return render(request,'register.html')



def verify_otp_host(request, email):
    if request.method == "POST":
        otp=request.POST.get('otp')
        hotel_host=HotelVendor.objects.get(email=email)

        if otp == hotel_host.otp:
            messages.success(request, "Login Success")
            login(request,hotel_host)
            return redirect('/accounts/host-login')
        
        messages.warning(request,"Wrong OTP")
        return redirect(f'/accounts/verify-otp-host/{email}/')
    

    return render(request, 'host/otp.html')



@login_required(login_url="host_login")
def host_dashboard(request):
    
    print("CURRENT USER:", request.user)
    print("USER ID:", request.user.id)

    stays = Hotel.objects.filter(hotel_owner=request.user)

    print("STAYS COUNT:", stays.count())
    print("ALL HOTELS:", Hotel.objects.all())

    context={'stays': Hotel.objects.filter(hotel_owner=request.user)}
    return render(request,"host/host_dashboard.html",context)


@login_required(login_url="host_login")
def host_add_stay(request):
    if request.method=="POST":
        hotel_name= request.POST.get('hotel_name')
        hotel_description=request.POST.get('hotel_description')
        ameneties= request.POST.getlist('ameneties')
        hotel_price=request.POST.get('hotel_price')
        hotel_offer_price=request.POST.get('hotel_offer_price')
        hotel_location=request.POST.get('hotel_location')
        hotel_slug= generateSlug(hotel_name)
        hotel_host=HotelVendor.objects.get(id=request.user.id)
    # print(
    #       f""" 
    #       {hotel_name,
    #       hotel_description,
    #       ameneties,
    #       hotel_price,
    #       hotel_offer_price,
    #       hotel_location,
    #       hotel_slug}"""
    #     )
        hotel_obj=Hotel.objects.create(
            hotel_name=hotel_name,
            hotel_description=hotel_description,
            hotel_price=hotel_price,
            hotel_offer_price=hotel_offer_price,
            hotel_location=hotel_location,
            hotel_slug=hotel_slug,
            hotel_owner=hotel_host
        )

        for amenety in ameneties:
            amenety= Ameneties.objects.get(id=amenety)
            hotel_obj.ameneties.add(amenety)
            hotel_obj.save()

        messages.success(request,"Hotel Created")
        return redirect(f'/accounts/host-dashboard')
    
    ameneties=Ameneties.objects.all()
    
    return render(request, 'host/host_add_stay.html', context={'ameneties': ameneties})


@login_required(login_url="host_login")
def host_upload_stay_images(request,slug):
    hotel_obj= Hotel.objects.get(hotel_slug=slug)
    if request.method == "POST":
        image=request.FILES['images']
        print(image)
        HotelImage.objects.create(
           hotel= hotel_obj,
           image=image
        )
        return HttpResponseRedirect(request.path_info)
    return render(request, 'host/host_upload_stay_images.html', context={
    "images": HotelImage.objects.filter(hotel=hotel_obj),
    "stay": hotel_obj
})


