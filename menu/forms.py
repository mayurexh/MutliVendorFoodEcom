from django import forms
from .models import *
from accounts.validators import allow_only_images
class CategoryForm(forms.ModelForm):
    
    
    class Meta:
        model = Category  
        fields = ["category_name", "description"]
        
        
class FoodItemForm(forms.ModelForm):
    image = forms.FileField(validators=[allow_only_images])
    class Meta:
        model = FoodItem
        fields = ["category","food_title","description","price","image","is_available"]