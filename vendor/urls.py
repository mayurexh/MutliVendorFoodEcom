from django.urls import path,include
from .import views
from accounts import views as acc_views
urlpatterns = [
    path('', acc_views.vendorDashboard, name= "vendorDashboard"),
    path('profile/', views.profile, name = "vprofile"),
    path('menu-builder/', views.menu_builder, name = "menu-builder"),
    path('menu-builder/category/<int:pk>', views.food_itemsby_category, name = "food_itemsby_category"),
    
    #category crud
    path('menu-builder/category/add', views.add_category, name= "add_category"),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name = "edit_category"),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name = "delete_category")

]