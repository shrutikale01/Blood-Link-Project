"""bloodbankmanagement URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from blood import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include app-specific URLs
    path('donor/', include('donor.urls')),
    path('hospital/', include('hospital.urls')),

    # Main views
    path('', views.home_view, name=''),
    path('logout', LogoutView.as_view(template_name='blood/logout.html'), name='logout'),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('adminlogin', LoginView.as_view(template_name='blood/adminlogin.html'), name='adminlogin'),

    # Admin Dashboard Views
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-blood', views.admin_blood_view, name='admin-blood'),
    path('admin-donor', views.admin_donor_view, name='admin-donor'),
    path('admin-hospital', views.admin_hospital_view, name='admin-hospital'),
    path('admin-donation', views.admin_donation_view, name='admin-donation'),
    path('admin-request', views.admin_request_view, name='admin-request'),
    path('admin-request-history', views.admin_request_history_view, name='admin-request-history'),

    # Update / Delete Views
    path('update-donor/<int:pk>/', views.update_donor_view, name='update-donor'),
    path('delete-donor/<int:pk>/', views.delete_donor_view, name='delete-donor'),
    path('update-hospital/<int:pk>/', views.update_hospital_view, name='update-hospital'),
    path('delete-hospital/<int:pk>/', views.delete_hospital_view, name='delete-hospital'),

    # Approve / Reject Donation
    path('approve-donation/<int:pk>/', views.approve_donation_view, name='approve-donation'),
    path('reject-donation/<int:pk>/', views.reject_donation_view, name='reject-donation'),

    # Approve / Reject Request Status
    path('update-approve-status/<int:pk>/', views.update_approve_status_view, name='update-approve-status'),
    path('update-reject-status/<int:pk>/', views.update_reject_status_view, name='update-reject-status'),

    # Dispatch Blood and Complete Donation
    path('dispatch-blood/<int:request_id>/', views.dispatch_blood, name='dispatch-blood'),
    path('complete-donation/<int:pk>/', views.complete_donation_view, name='complete-donation'),
    path('edit-donation-camp/<int:camp_id>/', views.edit_donation_camp, name='edit-donation-camp'),
    path('delete-donation-camp/<int:camp_id>/', views.delete_donation_camp, name='delete-donation-camp'),
    path('admin-donation-camps/', views.donation_camps_list_view, name='admin-donation-camps'),
    path('add-donation-camp/', views.add_donation_camp, name='add-donation-camp'),
]
