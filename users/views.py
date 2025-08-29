from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from listing.models import Listing, City, SubCity
import requests
from django.conf import settings
import os

RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')

def get_landing(request):
    featured_listings = Listing.objects.filter(admin_status=True).order_by('-created_at')[:3]
    
    context = {
        'featured_listings':featured_listings,
    }
    return render(request,'landing.html', context)



def register(request):
    if request.method == 'POST':   
        # Get CAPTCHA response
        captcha_token = request.POST.get('g-recaptcha-response')
        captcha_secret = RECAPTCHA_SECRET_KEY 

        # Verify with Google
        captcha_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': captcha_secret,
                'response': captcha_token
            }
        )
        result = captcha_response.json()

        if not result.get('success'):
            form = UserRegistrationForm(request.POST)
            context = {
                'form': form,
                'error': 'Invalid reCAPTCHA. Please try again.'
            }
            return render(request, 'auth/register.html', context)
        
        if request.POST.get('nickname'):
            context = {
                'form': form,
                'error': 'Bot Detected'
            }
            return render(request, 'auth/register.html', context)

        # CAPTCHA passed — continue with registration
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('listings')
    else:
        form = UserRegistrationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    form = UserLoginForm()
    context = {
        'form':form
    }
    if request.method == 'POST':
        # Handle login form submission
        email = request.POST['email']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            if request.user.is_admin:
                return redirect('admin-dashboard')
            return redirect('listings')
        else:
            # Invalid credentials
            context = {
                'form':form,
                'error': 'Invalid credentials'
            }
            return render(request, 'auth/login.html',context)
            # return redirect('login_view')
    else:
        return render(request, 'auth/login.html',context)

def logout_view(request):
    logout(request)
    if request.user.is_staff:
        return redirect('login')
    return redirect('listings')

@login_required 
def home_view(request):
    return render(request,'home.html', {'id': request.user.id})

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_email = form.cleaned_data['email']
            new_first_name = form.cleaned_data['first_name']
            new_last_name = form.cleaned_data['last_name']
            new_password = form.cleaned_data['new_password']

            if user.check_password(old_password):
                user.email = new_email
                user.first_name = new_first_name
                user.last_name = new_last_name
                if new_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Profile updated successfully.')
                    return redirect('profile_update_view')
            else:
                messages.error(request, 'Incorrect old password. Profile update failed.')
    else:
        form = ProfileUpdateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'user/profile_update.html', {'form': form})
