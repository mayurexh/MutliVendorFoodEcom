from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from accounts.forms import UserForm, UserProfileForm
from .forms import VendorForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify


def get_vendor(request):
    vendor = Vendor.objects.get(user = request.user)
    return vendor

# Create your views here.
@login_required
@user_passes_test(check_role_vendor)
def profile(request):
    profile = get_object_or_404(UserProfile, user = request.user)
    vendor = get_object_or_404(Vendor, user = request.user)
    
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES,instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Profile Updated Successfully")
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
        
    context = {
        'profile_form' : profile_form,
        'vendor_form' : vendor_form,
        'profile':profile,
        'vendor':vendor
    }
    return render(request,"vendor/vprofile.html", context)


@login_required
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor = vendor).order_by("created_at")
    context = {
        'categories':categories
    }
    return render(request, 'vendor/menu-builder.html',context)


@login_required
@user_passes_test(check_role_vendor)
def food_itemsby_category(request,pk):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk = pk)
    fooditems = FoodItem.objects.filter(vendor = vendor, category = category)

    context = {"fooditems":fooditems, "category":category}
    return render(request, "vendor/food_itemsby_category.html",context)

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST) #request.POST will contain the POST (category_name, description) coming from the frontend
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            #assign vendor and slug to the category before saving the data
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, "Your category has been saved!")
            return redirect("menu-builder")
        else:
            messages.error(request, "Invalid form data")
    else:
        form = CategoryForm()
     
    
    context = {
        "form":form
    }
    return render(request, "vendor/add_category.html", context)

def edit_category(request, pk= None):
    category = get_object_or_404(Category, pk = pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category) #request.POST will contain the POST (category_name, description) coming from the frontend
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            #assign vendor and slug to the category before saving the data
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, "Your category has been saved!")
            return redirect("menu-builder")
        else:
            messages.error(request, "Invalid form data")
    else:
        form = CategoryForm(instance=category)
     
    
    context = {
        "form":form,
        "category": category
    }
    return render(request, "vendor/edit_category.html", context)


@login_required
@user_passes_test(check_role_vendor)
def delete_category(request,pk = None):
    category = get_object_or_404(Category, pk = pk)
    category.delete()
    messages.success(request, "The category has been deleted")
    return redirect("menu-builder")


@login_required
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES) #request.POST will contain the POST (category_name, description) coming from the frontend
        if form.is_valid():
            food_title = form.cleaned_data["food_title"]
            #assign vendor and slug to the category before saving the data
            fooditem = form.save(commit=False)
            fooditem.vendor = get_vendor(request)
            fooditem.slug = slugify(food_title)
            fooditem.save()
            messages.success(request, "Your category has been saved!")
            return redirect("food_itemsby_category",fooditem.category.id)
        else:
            messages.error(request, "Invalid form data")
    else:
        form = FoodItemForm()
        #overwrite the queryset of category which give category for all users instead of the requested one
        form.fields["category"].queryset = Category.objects.filter(vendor = get_vendor(request))
     
    context= {"form":form}
    return render(request, "vendor/add_food.html",context)


def edit_food(request,pk = None):
    food_item = FoodItem.objects.get(pk = pk)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=food_item) #request.POST will contain the POST (category_name, description) coming from the frontend
        if form.is_valid():
            food_title = form.cleaned_data["food_title"]
            #assign vendor and slug to the category before saving the data
            fooditem = form.save(commit=False)
            fooditem.vendor = get_vendor(request)
            fooditem.slug = slugify(food_title)
            fooditem.save()
            messages.success(request, "Your category has been saved!")
            return redirect("food_itemsby_category",fooditem.category.id)
        else:
            messages.error(request, "Invalid form data")
    else:
        form = FoodItemForm(instance=food_item)
        form.fields["category"].queryset = Category.objects.filter(vendor = get_vendor(request))
        
     
    context= {"form":form,
              "food_item":food_item}
    
    
    return render(request, "vendor/edit_food.html", context)
    
    
    
def delete_food(request, pk = None):
    food_item = FoodItem.objects.get(pk=pk)
    category = food_item.category
    category_id = category.id
    food_item.delete()
    return redirect("food_itemsby_category",category_id )