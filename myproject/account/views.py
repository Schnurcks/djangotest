from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import login
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib.auth.models import User
import time

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from . tokens import generate_token

@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',{'section': 'dashboard'})

def sent_activation_link(user, site):
     # Email Address Confirmation Email
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            
            email_subject = "Confirm your email for schnurcks.de"

            message = render_to_string('account/email_confirmation.html',{
                
                'name': user.username.capitalize(),
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user),
            })

            send_mail(email_subject, message, from_email, to_list, fail_silently=True)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
    
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            # Save the User object
            new_user.save()

            # Create the user profile
            Profile.objects.create(user=new_user)          
            current_site = get_current_site(request)

            sent_activation_link(new_user, current_site)

            return render(request, 'account/register_done.html',{'new_user': new_user, 'section': 'register'})
    
    else:
        user_form = UserRegistrationForm()
    
    return render(request,'account/register.html',{'user_form': user_form, 'section': 'register'})

def resend_activation(request):  

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email').lower()
            
            try:
                user = User.objects.get(email__exact=user_email)
                print(f'USER >> {user}')
                current_site = get_current_site(request)
                sent_activation_link(user, current_site)
            except:
                print('USER does not exist') 
            
            messages.success(request, 'If the email address is valid an activation link was sent, if you don''t receive an email please check your email address and try again')
        
        else:
            messages.error(request, 'Please enter a valid email adress')

    form = PasswordResetForm()
    return render(request,'account/resend_activation.html', {'form': form })

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        new_user = None

    if new_user is not None and generate_token.check_token(new_user,token):
        if new_user.is_active:
            messages.warning(request, "Your account has already been activated!")    
        else:
            new_user.is_active = True
            new_user.save()
            login(request,new_user)
            messages.success(request, "Your account had been activated! In case you cannot login please try a passowrd reset!")
        return render(request,'account/dashboard.html',{'section': 'dashboard'})
    else:
        messages.error(request, 'Your account could not be activated! If you want to resent the activation link click <a href="/activationlink">here</a>' )
        return render(request,'account/dashboard.html',{'section': 'dashboard'})
     
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
        instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form, 'section': 'edit'})