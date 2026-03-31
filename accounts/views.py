from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import forms as auth_forms, login, get_user_model
from django.contrib import messages

User = get_user_model()

from .models import Follow
from posts.models import Post

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

@login_required
def profile(request, username):
    """View to see a user's public profile and their posts."""
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    
    is_following = Follow.objects.filter(
        follower=request.user, following=profile_user
    ).exists()
    
    followers_count = profile_user.follower_set.count()
    following_count = profile_user.following_set.count()

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    })

@login_required
def follow_toggle(request, username):
    """View for toggling following a user."""
    if request.method == 'POST':
        target = get_object_or_404(User, username=username)
        if target != request.user:
            follow, created = Follow.objects.get_or_create(
                follower=request.user, following=target
            )
            if not created:
                follow.delete()
    return redirect('profile', username=username)

