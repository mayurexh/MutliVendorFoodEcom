from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings

def detect_user(user):
    if user.role ==1:
        redirectUrl = "vendorDashboard"
        return redirectUrl
    elif user.role == 2:
        redirectUrl = "customerDashboard"
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = "/admin"
        return redirectUrl
    
def send_verification_email(request,user):
    current_site = get_current_site(request)
    mail_subject = "Please verify your account"
    message = render_to_string("accounts/emails/account_verify_email.html",{
        "user":user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.send()
    
    
def password_reset_link(request,user):
    current_site = get_current_site(request)
    mail_subject = "Reset your password"
    message = render_to_string("accounts/emails/reset_password_email.html",{
        "user":user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.send()
    

def send_notificaton_mail(mail_subject, mail_template, context):
    message = render_to_string(mail_template, context)
    to_email = context['user'].email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.send()
