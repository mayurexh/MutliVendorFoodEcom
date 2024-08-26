from django.contrib import admin
from .models import Category, FoodItem


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ['category_name', 'vendor']
    search_fields = ['category_name', "vendor__vendor_name"]


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('food_title',)}
    list_display = ["category","food_title","price","image","vendor", "is_available"]
    search_fields = ["category__category_name","vendor__vendor_name","is_available"]
    list_filter = ('is_available',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)


# Register your models here.
