from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import RequestsForm


def homepage(request):
    return render(request, 'webside/home.html',{})

def requests(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'webside/requests.html', {'posts': posts})

def requests_detail(request, pk):
    post= get_object_or_404(Post, pk=pk)
    return render(request, 'webside/requests_detail.html', {'post': post})

def requests_new(request):
    if request.method == "POST":
        form = RequestsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('requests_detail', pk=post.pk)
    else:
        form = RequestsForm()
    return render(request, 'webside/requests_edit.html', {'form': form})
