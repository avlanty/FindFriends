from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post

# Create your views here.
@login_required(login_url='login')
def create_post(request):
    if request.method == "POST":
        content = request.POST.get('content', '')
        if content:
            try:
                Post.objects.create(member=request.user, content=content)
                messages.success(request, "Post created!")
            except Exception:
                messages.error(request, "Post failed to create, try again.")
                return render(request, "posts/create_post.html", {'posts': content})
        return redirect("index")
    return render(request, "posts/create_post.html")