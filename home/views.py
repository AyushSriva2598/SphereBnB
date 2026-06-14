from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import Hotel, Ameneties, Booking
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import date
from accounts.utils import bookingConfirmationEmail


def index(request):

    hotels = Hotel.objects.prefetch_related(
        'ameneties',
        'hotel_images'
    ).filter(is_active=True)

    search = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    amenity_id = request.GET.get('amenity')

    # Search
    if search:
        hotels = hotels.filter(
            Q(hotel_name__icontains=search) |
            Q(hotel_location__icontains=search) |
            Q(hotel_description__icontains=search)
        )

    # Min Price
    if min_price:
        hotels = hotels.filter(
            hotel_offer_price__gte=min_price
        )

    # Max Price
    if max_price:
        hotels = hotels.filter(
            hotel_offer_price__lte=max_price
        )

    # Amenity Filter
    if amenity_id:
        hotels = hotels.filter(
            ameneties__id=amenity_id
        )

    hotels = hotels.distinct()[:20]

    amenities = Ameneties.objects.all()

    return render(
        request,
        "index.html",
        {
            "hotels": hotels,
            "amenities": amenities,
            "search": search or "",
            "min_price": min_price or "",
            "max_price": max_price or "",
            "selected_amenity": amenity_id or "",
        }
    )

def hotel_details(request, slug):

    hotel = get_object_or_404(
        Hotel.objects.prefetch_related('ameneties','hotel_images'),
        hotel_slug=slug
    )

    return render(request, 'hotel_details.html',context={'hotel': hotel})

# /check-availability/<slug>/?check_in=...&check_out=...
def _is_available(hotel, check_in, check_out, exclude_booking_id=None):
    """
    Return True if no *confirmed* or *pending* booking overlaps the
    requested window. Cancelled bookings are ignored so those dates
    become available again.
    """
    qs = Booking.objects.filter(
        hotel=hotel,
        status__in=["confirmed", "pending"],   # ignore cancelled
        check_in__lt=check_out,
        check_out__gt=check_in,
    )
    if exclude_booking_id:
        qs = qs.exclude(id=exclude_booking_id)
    return not qs.exists()
 
 
# ── views ──────────────────────────────────────────────────────────────────
 
def check_availability(request, slug):
    hotel = get_object_or_404(Hotel, hotel_slug=slug)
    check_in  = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
 
    if not check_in or not check_out:
        return JsonResponse({"available": False, "error": "Missing dates."}, status=400)
 
    available = _is_available(hotel, check_in, check_out)
    return JsonResponse({"available": available})
 
 
@login_required(login_url="login_view")
def create_reservation(request, slug):
    hotel = get_object_or_404(Hotel, hotel_slug=slug)
 
    if request.method == "POST":
        check_in  = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        guests    = request.POST.get('guests')
 
        # ── server-side validation (never trust the client) ────────────────
        try:
            ci = date.fromisoformat(check_in)
            co = date.fromisoformat(check_out)
        except (TypeError, ValueError):
            messages.error(request, "Invalid dates. Please try again.")
            return redirect('reserve_stay', slug=slug)
 
        if ci >= co:
            messages.error(request, "Check-out must be after check-in.")
            return redirect('reserve_stay', slug=slug)
 
        if ci < date.today():
            messages.error(request, "Check-in cannot be in the past.")
            return redirect('reserve_stay', slug=slug)
 
        # ── re-check availability atomically ───────────────────────────────
        if not _is_available(hotel, check_in, check_out):
            messages.error(
                request,
                "Those dates are unavailable. Please choose different dates."
            )
            return redirect('reserve_stay', slug=slug)
 
        # ── dates are free → confirm immediately, no host approval needed ──
        booking=Booking.objects.create(
            hotel=hotel,
            guest=request.user,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            status="confirmed",          # ← auto-confirmed
        )
        email=booking.guest.email
        bookingConfirmationEmail(email,booking)
        messages.success(request, "You're all set! Your stay has been confirmed.")
        return redirect('/')
 
    return render(request, "reserve_stay.html", {"hotel": hotel})
 
 
@login_required(login_url="host_login")
def host_update_booking_status(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)
 
    if request.user.id != booking.hotel.hotel_owner.id:
        return HttpResponse("You are not authorised", status=403)
 
    if action == "confirm":
        booking.status = "confirmed"
        messages.success(request, "Reservation approved.")
    elif action == "cancel":
        booking.status = "cancelled"
        messages.success(request, "Reservation cancelled.")
    else:
        return HttpResponse("Invalid action.", status=400)
 
    booking.save()
    return redirect('/accounts/host-dashboard/')
 

@login_required
def user_profile(request):

    bookings = Booking.objects.filter(guest=request.user).order_by("-id")

    return render(request,"profile.html",{"bookings": bookings})