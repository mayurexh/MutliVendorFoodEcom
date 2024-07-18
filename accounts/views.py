from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import *
from django.contrib import messages

# Create your views here.

def registerUser(request):
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
            messages.success(request, "User registered successfully")
            print('user is created from views')
            return redirect("registerUser")
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {
        "form":form,
        "msg": "Registeration Failed"
    }
    return render(request,"accounts/registerUser.html",context)

