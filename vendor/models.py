from django.db import models
from accounts.models import *
from accounts.utils import send_notificaton_mail
#vendor model
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="userprofile")
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to="vendor/license")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vendor_name
    
    def save(self, *args , **kwargs) -> None:
        if self.pk is not None:
            #update
            origin = Vendor.objects.get(pk = self.pk)
            if origin.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                'user' : self.user,
                'is_approved': self.is_approved
                } 
                if self.is_approved == True:
                    mail_subject = "Your restaurent has been approved"
                    send_notificaton_mail(mail_subject, mail_template, context)
                elif self.is_approved == False:
                    mail_subject = "Your restaurent is yet to be approved"
                    send_notificaton_mail(mail_subject, mail_template, context)
        return super(Vendor,self).save(*args, **kwargs)