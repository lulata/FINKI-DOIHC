from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from .models import Post, Block, Profile
from .forms import PostForm, BlockForm

# Create your views here.

def posts(request: WSGIRequest):
    blockedUsers = Block.objects.filter(blocked=request.user).values_list("blocked", flat=True)
    postsVisible = Post.objects.exclude(author__user__in=blockedUsers)

    return render(request, "posts.html", {"posts": postsVisible})


def profile(request: WSGIRequest):
    user = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(author=user)

    return render(request, "profile.html", {"posts": posts, "user": user})



def add(request: WSGIRequest):
    if request.method == "POST":
        form_data = PostForm(data=request.POST, files=request.FILES)

        if form_data.is_valid():
            post = form_data.save(commit=False)
            post.author = Profile.objects.get(user=request.user)
            post.save()

            return redirect("posts")
        

    return render(request, "add-form.html", {"form": PostForm})


def blocked(request: WSGIRequest):
    if request.method == "POST":
        form_data = BlockForm(data=request.POST, files=request.FILES)

        if form_data.is_valid():
            block = form_data.save(commit=False)
            block.blocker = Profile.objects.get(user=request.user)
            block.save()

            return redirect("blocked")

    blocks = Block.objects.filter(blocker=request.user)
    blockedUsers = Profile.objects.filter(user__in=blocks.values_list("blocked", flat=True))

    return render(request, "profile-block.html", {"form": BlockForm, "users": blockedUsers})