from typing import Any
from django import forms
from .models import *
from vendor.models import Vendor
from .validators import allow_only_images
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["first_name","last_name", "username", "email","phone_number","password"]

    def clean(self) -> dict[str, Any]:
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password!=confirm_password:
            raise forms.ValidationError("Password doesnot match")


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(validators= [allow_only_images])
    cover_photo = forms.FileField(validators= [allow_only_images])
    latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start typing...', 'required':'required'}))
    
    
    class Meta: 
        model = UserProfile
        fields = ['profile_picture','cover_photo','address','country','state','city', 'pin_code','latitude','longitude']