import os
from django.core.exceptions import ValidationError

def allow_only_images(file):
    ext = os.path.splitext(file.name)[1]
    allowed = ['.png', '.jpg', '.jpeg']
    if ext.lower() not in allowed:
        raise ValidationError("Not a valid file type. Allowed file types are: "+str(allowed))