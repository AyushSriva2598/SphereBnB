from django.urls import path
from accounts import views
urlpatterns = [
    path('login/',views.login_view,name='login_view'),
    path('register/',views.register_view,name='register_view'),
    path('logout/',views.logout_view,name='logout_view'),
    path('send-otp/',views.send_OTP, name='send_OTP'),
    path('verify-otp/<email>/',views.verify_otp, name='verify_otp'),
    path('verify-account/<token>/',views.verify_email_token,name='verify_email_token'),
    path('host-login/',views.host_login,name='host_login'),
    path('host-logout/',views.host_logout,name='host_logout'),
    path('host-register/',views.host_register,name='host_register'),
    path('send-otp-host/',views.send_OTP_host, name='send_OTP_host'),
    path('verify-otp-host/<email>/',views.verify_otp_host, name='verify_otp_host'),
    path('verify-account-host/<token>/',views.verify_email_token_host,name='verify_email_token_host'),
    path('host-dashboard/',views.host_dashboard,name='host_dashboard'),
    path('host-add-stay/',views.host_add_stay,name='host_add_stay'),
    # path('<slug>/host-upload-stay-images/',views.host_upload_stay_images,name='host_upload_stay_images'),
    path('delete-stay-image/<id>/',views.host_delete_stay_image,name='host_delete_stay_image'),
    path('<slug>/host-edit-stay/',views.host_edit_stay,name='host_edit_stay'),
]   