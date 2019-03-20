from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Comment, Loan, Community, Trade_request, Trade_loan
from .forms import RequestsForm, CommentForm, LoansForm, CommentForm2, CommunityForm, SignUpForm, ReportForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from . import forms
from .tokens import account_activation_token
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import json

def homepage(request):
    return render(request, 'webside/home.html',{})

def requests(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    query=request.GET.get('q')
    if query:
        posts=posts.filter(
        Q(title__icontains=query)|
        Q(text__icontains=query)|
        Q(community__name__icontains=query)
        ).distinct()
    paginator=Paginator(posts, 5)
    page= request.GET.get('page')
    try:
        items=paginator.page(page)
    except PageNotAnInteger:
        items=paginator.page(1)
    except EmptyPage:
        items=paginator.page(paginator.num_pages)
    context={
        'items': items
    }
    return render(request, 'webside/requests.html', context)

def requests_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        if 'report_post' in request.POST:
            form = ReportForm(request.POST)
            if form.is_valid():
                report = form.save(commit=False)
                report.user1 = request.user
                report.user2 = post.author
                report.save()
                return redirect('requests_detail', pk=post.pk)
        elif 'report_comment' in request.POST:
            form = ReportForm(request.POST)
            if form.is_valid():
                report = form.save(commit=False)
                report.user1 = request.user
                report.user2 = request.comment.author
                report.save()
                return redirect('requests_detail', pk=post.pk)
    else:
        form = ReportForm()
    if request.method == "GET" and request.is_ajax():
        data_string = request.GET.get('rating')
        auth = request.GET.get('auth')
        u2 = User.objects.get(username=auth)
        trade = Trade_request(giver = request.user, receiver = u2, rating = data_string, post = post)
        trade.save()
        request.user.profile.given += 1
        request.user.save()
        u2.profile.gotten += 1
        u2.save()
        post.active = False
        post.save()
        return redirect('requests')
    return render(request, 'webside/requests_detail.html', {'post': post, 'form': form})

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

def loans(request):
    loans=Loan.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    query=request.GET.get('q')
    if query:
        loans=loans.filter(
        Q(title__icontains=query)|
        Q(text__icontains=query)|
        Q(community__name__icontains=query)
        ).distinct()
    paginator=Paginator(loans, 5)
    page= request.GET.get('page')
    try:
        items=paginator.page(page)
    except PageNotAnInteger:
        items=paginator.page(1)
    except EmptyPage:
        items=paginator.page(paginator.num_pages)
    context={
        'items': items
    }
    return render(request, 'webside/loans.html', context)

def loans_detail(request, pk):
    loan= get_object_or_404(Loan, pk=pk)
    print("2")
    if request.method == "POST":
        if 'report_loan' in request.POST:
            form = ReportForm(request.POST)
            if form.is_valid():
                report = form.save(commit=False)
                report.user1 = request.user
                report.user2 = loan.author
                report.save()
            return redirect('loans_detail', pk=loan.pk)
        elif 'report_comment' in request.POST:
            form = ReportForm(request.POST)
            if form.is_valid():
                report = form.save(commit=False)
                report.user1 = request.user
                report.user2 = request.user
                report.save()
                return redirect('loans_detail', pk=loan.pk)
    else:
        form = ReportForm()
    if request.method == "GET" and request.is_ajax():
        print("ajax")
        data_string = request.GET.get('rating')
        auth = request.GET.get('auth')
        u2 = User.objects.get(username=auth)
        trade = Trade_loan(giver = request.user, receiver = u2, rating = data_string, loan = loan)
        trade.save()
        request.user.profile.given += 1
        request.user.save()
        u2.profile.gotten += 1
        u2.save()
        loan.active = False
        loan.save()
        return redirect('loans')
    return render(request, 'webside/loans_detail.html', {'loan': loan, 'form': form})

def loans_new(request):
    if request.method == "POST":
        form = LoansForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.author = request.user
            loan.published_date = timezone.now()
            loan.save()
            return redirect('loans_detail', pk=loan.pk)
    else:
        form = LoansForm()
    return render(request, 'webside/loans_edit.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            from_email = settings.EMAIL_HOST_USER
            to_email = form.cleaned_data.get('email')
            mail_subject = 'Aktiver kontoen din til ShareBoi'
            mail_message = render_to_string('webside/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            send_mail(mail_subject, mail_message, from_email, [to_email, settings.EMAIL_HOST_USER], fail_silently = False)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    form.fields['username'].label = "Brukernavn"
    form.fields['password1'].label = "Passord"
    form.fields['password2'].label = "Bekreft passord"
    form.fields['gender'].label = "Kjønn"
    form.fields['age'].label = "Alder"
    for fieldname in ['username', 'password1', 'password2']:
            form.fields[fieldname].help_text = None
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
            comment.author = request.user
            comment.save()
            return redirect('requests_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'webside/add_comment_to_post.html', {'form': form})

def add_comment_to_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == "POST":
        form = CommentForm2(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.loan = loan
            comment.author = request.user
            comment.save()
            return redirect('loans_detail', pk=loan.pk)
    else:
        form = CommentForm2()
    return render(request, 'webside/add_comment_to_loan.html', {'form': form})

def add_community(request):
    if request.method == "POST":
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.save()
            return redirect('communitylist')
    else:
        form = CommunityForm()
    return render(request, 'webside/add_community.html', {'form': form})

def communitylist(request):
    communities=Community.objects.all()
    return render(request, 'webside/communitylist.html', {'communities': communities})


def showmap(request):
    loans=Loan.objects.all()
    communities=Community.objects.all()
    if request.method == "POST":
        form = PickCommunity(request.POST)
    else:
        form = PickCommunity()
    return render(request, 'webside/showmap.html', {'loans': loans, 'communities': communities, 'form': form})

def loan_delete(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    loan.delete()
    return redirect('loans')

def request_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('requests')
