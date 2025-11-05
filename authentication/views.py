from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse


def login(request):
    """Login view"""
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('load:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login successful
            auth_login(request, user)
            
            # Set session expiry
            if not remember:
                request.session.set_expiry(0)  # Session expires when browser closes
            else:
                request.session.set_expiry(1209600)  # 2 weeks
            
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to next page or dashboard
            next_url = request.GET.get('next', 'load:index')
            return redirect(next_url)
        else:
            # Login failed
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'login.html')


@login_required
def logout(request):
    """Logout view"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('authentication:login')


def register(request):
    """Register view (placeholder)"""
    # TODO: Implement registration functionality
    return render(request, 'register.html')


def forgot_password(request):
    """Forgot password view (placeholder)"""
    # TODO: Implement password reset functionality
    return render(request, 'forgot_password.html')
