from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

@login_required
def post_list(request):
    """View to list all posts."""
    posts = Post.objects.all().select_related('author').order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    """View to see post details. No comments at this stage."""
    post = get_object_or_404(Post.objects.select_related('author'), pk=pk)
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
    """Redirect home to list of posts if logged in."""
    if request.user.is_authenticated:
        return redirect('post-list')
    return redirect('login')
