from django.shortcuts import render
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .forms import UserLoginForm

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
            return redirect('home')
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
            return redirect('home')
        else:
            # Invalid credentials
            context = {
                'form':form,
                'error': 'Invalid credentials'
            }
            return render(request, 'auth/login.html',context)
            return redirect('login_view')
    else:
        return render(request, 'auth/login.html',context)

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request,'home.html', {'id': request.user.id})