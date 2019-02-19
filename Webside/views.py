from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import RequestsForm, CommentForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from . import forms
from .tokens import account_activation_token


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

@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        form.fields['username'].label = "Brukernavn"
        form.fields['password1'].label = "Passord"
        form.fields['password2'].label = "Bekreft passord"
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Aktivere kontoen din til ShareBoi'
            message = render_to_string('webside/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = forms.SignUpForm()
    form.fields['username'].label = "Brukernavn"
    form.fields['password1'].label = "Passord"
    form.fields['password2'].label = "Bekreft passord"
    return render(request, 'webside/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'webside/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'webside/account_activation_invalid.html')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('requests_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'webside/add_comment_to_post.html', {'form': form})
