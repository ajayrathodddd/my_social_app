from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Post

from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post

def profile_view(request, username):
    # Fetch user or show 404
    profile_user = get_object_or_404(User, username=username)
    # Get all posts created by this user
    user_posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    
    context = {
        'profile_user': profile_user,
        'user_posts': user_posts,
    }
    return render(request, 'feed/profile.html', context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "feed/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after registration
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'feed/register.html', {'form': form})

def home_view(request):
    return render(request, 'feed/index.html')


def get_posts_api(request):
    """API endpoint to get all posts in JSON format"""
    posts = (
        Post.objects.select_related("author").all().order_by("-created_at")
    )

    serialized_data = [
        {
            "id": post.id,
            "author": post.author.username,
            "content": post.content,
            "image": post.image.url if post.image else None,
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "total_likes": post.total_likes(),
        }
        for post in posts
    ]

    return JsonResponse({"posts": serialized_data})


@csrf_exempt
def create_post_api(request):
    """API endpoint to create a post"""
    if request.method == "POST":
        content = request.POST.get("content")
        image = request.FILES.get("image")

        if content and request.user.is_authenticated:
            post = Post.objects.create(
                author=request.user, content=content, image=image
            )
            return JsonResponse(
                {
                    "message": "Post created successfully",
                    "post_id": post.id,
                },
                status=201,
            )

        return JsonResponse({"error": "Content required or user not logged in"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def like_post_api(request, post_id):
    """API endpoint to like/unlike a post"""
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse(
            {"liked": liked, "total_likes": post.total_likes()}
        )

    return JsonResponse({"error": "Authentication required"}, status=401)