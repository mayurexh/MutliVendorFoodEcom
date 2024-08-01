from django.urls import path,include
from .import views
from accounts import views as acc_views
urlpatterns = [
    path('', acc_views.vendorDashboard, name= "vendorDashboard"),
    path('profile/', views.profile, name = "vprofile")
    
]