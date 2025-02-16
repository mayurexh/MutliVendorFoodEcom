from django import forms
from .models import *
from accounts.validators import allow_only_images
class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(validators= [allow_only_images])
    class Meta:
        model = Vendor
        fields = ["vendor_name", "vendor_license"]