from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import Hotel, Ameneties
from django.db.models import Q
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