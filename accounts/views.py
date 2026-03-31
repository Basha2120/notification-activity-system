from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import forms as auth_forms, login, logout
from django.contrib import messages

def register(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = auth_forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = auth_forms.UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
