from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('hotel-details/<slug>/',views.hotel_details,name='hotel_details'),
    path('check-availability/<slug>/', views.check_availability, name='check_availability'),    
    path('create-reservation/<slug>/',views.create_reservation,name='create_reservation'),
    path('booking/<int:booking_id>/<str:action>/', views.host_update_booking_status, name='host_update_booking_status'),
    path("profile/",views.user_profile,name="user_profile"),
    
    
]