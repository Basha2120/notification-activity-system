from django.shortcuts import render, redirect
from django.contrib.auth import forms as auth_forms, login
from django.contrib import messages

def register(request):
    """Registration view for new users."""
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = auth_forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            # Redirection to feed or posts list
            return redirect('/')
    else:
        form = auth_forms.UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
