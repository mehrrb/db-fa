from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
            
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')


@login_required
def register_view(request):
    # Only allow superusers to register new users
    if not request.user.is_superuser:
        messages.error(request, 'شما دسترسی لازم برای این صفحه را ندارید.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'کاربر جدید با موفقیت ایجاد شد.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'users/register.html', {'form': form})
