from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Follow
from .models import Post, Comment

@login_required
def feed(request):
    """Personalized activity feed: posts from users you follow."""
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list('following_id', flat=True)

    posts = (
        Post.objects
        .filter(author_id__in=following_ids)
        .select_related('author')
        .prefetch_related('comments')
        .order_by('-created_at')
    )
    return render(request, 'posts/feed.html', {'posts': posts})

@login_required
def post_list(request):
    """View to list all posts."""
    posts = Post.objects.all().select_related('author').prefetch_related('comments').order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    """View to see post details and add comments."""
    post = get_object_or_404(Post.objects.select_related('author').prefetch_related('comments__author'), pk=pk)
    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            Comment.objects.create(post=post, author=request.user, body=body)
            return redirect('post-detail', pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def create_post(request):
    """View to create a new post."""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()
        if title and body:
            Post.objects.create(author=request.user, title=title, body=body)
            return redirect('post-list')
    return render(request, 'posts/create_post.html')

def home(request):
    """Redirect home to personal feed if logged in."""
    if request.user.is_authenticated:
        return redirect('feed')
    return redirect('login')
