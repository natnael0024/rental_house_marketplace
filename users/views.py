from django.shortcuts import render
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    if request.method == 'POST':   
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        # username = request.POST['username']
        # password = request.POST['password']
        # user = CustomUser.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('listings')
    else:
        form = UserRegistrationForm()
        context = {
            'form':form
        }
        return render(request, 'auth/register.html',context)

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
