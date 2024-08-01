from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import *
from vendor.models import Vendor
from django.contrib import messages, auth
from vendor.models import Vendor
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required,user_passes_test
from .utils import detect_user, send_verification_email, password_reset_link
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
#custom decorator to restrict vendor from accessing customer
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


#custom decorator to restrict customer from accessing vendor
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        return redirect("myAccount")
    msg = ""
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # user.set_password(password)
            # form.save()

            #create user using create_user method
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = form.cleaned_data["username"]
            user = User.objects.create_user(first_name = first_name,last_name= last_name,username = username, email= email, password=password)
            user.role = User.CUSTOMER 
            user.save()
            
            #user verification
            send_verification_email(request,user)
            
            
            messages.success(request, "User registered successfully")
            print('user is created from views')
            return redirect("registerUser")
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {
        "form":form,
    }
    return render(request,"accounts/registerUser.html",context)



def registerVendor(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = form.cleaned_data["username"]
            user = User.objects.create_user(first_name = first_name,last_name= last_name,username = username, email= email, password=password)
            user.role = User.VENDOR 
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user = user)
            vendor.user_profile = user_profile
            vendor.save()
            
            #vendor verification
            send_verification_email(request, user)
            
            
            messages.success(request,"Account registered successfully please wait for approval")
            return redirect("registerVendor")
            
        else:
            print("Invalid Form")
            print(form.errors)
        
    
    form = UserForm()
    v_form = VendorForm()
    return render(request, "accounts/registerVendor.html", {"form":form,
                                                            "v_form":v_form})
    

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "Wait you are already logged in")
        return redirect("myAccount")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate( email = email, password = password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in")
            return redirect("myAccount")
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("login")
    return render(request, 'accounts/login.html')

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.info(request, "you are logged out")
    return redirect("login")


@login_required(login_url="login")
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, "accounts/customerDashboard.html")



@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user = request.user)
    context = {'vendor':vendor}
    return render(request, "accounts/vendorDashboard.html", context)

@login_required(login_url="login")
def myAccount(request):
    user = request.user
    redirectUrl = detect_user(user)
    return redirect(redirectUrl)


def activate(request, uidb64, token):
    try:    
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations your account has been activated")
        return redirect("myAccount")
    else:
        messages.error(request, "invalid activation link")
        return redirect("myAccount")

def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email__exact = email)
            password_reset_link(request, user)
            messages.success(request, "Password reset link has been send to your email address")
            return redirect("login")
        else:
            messages.error(request, "Account does not exist")
            return redirect("forgot_password")
    return render(request, "accounts/forgot_password.html")


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(ValueError, User.DoesNotExist,OverflowError, TypeError):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request, "Please reset your password")
        return redirect("reset_password")
    else:
        messages.error(request, "This link has been expired")
        return redirect("myAccount")
    


def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            pk = request.session.get("uid")
            user = User.objects.get(pk = pk )
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password changed successfully")
            return redirect("login")
        else:
            messages.error(request, "Password does not match")
            return redirect("reset_password")
    return render(request, "accounts/reset_password.html")








# def change_password(request):
#     user = request.user
#     password_reset_link(request,user)
#     return HttpResponse("CHECK MAIL")

# def password_reset(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User._default_manager.get(pk = uid)
#     except(ValueError, User.DoesNotExist,OverflowError, TypeError):
#         user = None
        
#     if user is not None and default_token_generator.check_token(user,token):
#         return HttpResponse("This is passworrd chnage page")
#     else:
#         messages.error(request, "Invalid password link")
#         return redirect("myAccount")
    
