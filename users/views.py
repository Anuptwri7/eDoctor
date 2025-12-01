from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from checkup.models import CheckupSubmission
from doctors.models import Doctor


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:

            print(form.errors)
            messages.error(request, 'Registration failed. Please check the form and try again.')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required
from setup.models import Banner
from django.shortcuts import render

@login_required
def home_view(request):
    user = request.user
    banners = Banner.objects.filter(is_active=True)
    total_doctors = Doctor.objects.count()

    total_checkups = CheckupSubmission.objects.filter(user=user).count()

    return render(request, 'users/home.html', {
        "banners": banners,
        "total_doctors": total_doctors,
        "total_checkups": total_checkups,
        "pending_reports": 3
    })
@login_required
def contact_view(request):
    return render(request, 'users/contact.html')

