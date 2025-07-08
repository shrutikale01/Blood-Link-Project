from django.urls import path

from django.contrib.auth.views import LoginView
from . import views
urlpatterns = [
    path('hospitallogin/', LoginView.as_view(template_name='hospital/hospitallogin.html'),name='hospitallogin'),
    path('hospitalsignup/', views.hospital_signup_view,name='hospitalsignup'),
     
    path('hospital/dashboard/', views.hospital_dashboard_view,name='hospitals-dashboard'),
    path('hospital/make-request/', views.make_request_view,name='make-request'),
    path('my-request/', views.my_request_view,name='my-request'),
   

]        