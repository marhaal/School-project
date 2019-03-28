from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from .forms import *
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
        u2 = User.objects.get(id=int(auth))
        trade = Trade_request(giver = u2, receiver = request.user, rating = data_string, post = post)
        post.active = False
        post.save()
        u2.profile.antallratet += 1
        u2.profile.sumratings += int(data_string)
        u2.profile.avgrating = (u2.profile.sumratings/u2.profile.antallratet)
        trade.save()
        request.user.profile.gotten += 1
        request.user.profile.sumkarma -= 1
        request.user.save()
        u2.profile.given += 1
        u2.profile.sumkarma += 4
        u2.save()
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
        u2 = User.objects.get(id=int(auth))
        trade = Trade_loan(giver = request.user, receiver = u2, rating = data_string, loan = loan)
        u2.profile.antallratet += 1
        u2.profile.sumratings += int(data_string)
        u2.profile.avgrating = (u2.profile.sumratings/u2.profile.antallratet)
        trade.save()
        request.user.profile.given += 1
        request.user.profile.sumkarma += 4
        request.user.save()
        u2.profile.gotten += 1
        u2.profile.sumkarma -= 1
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
            user.profile.gender = form.cleaned_data['gender']
            user.profile.age = form.cleaned_data['age']
            user.profile.community = form.cleaned_data['community']
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
    form.fields['community'].label = "Område"
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
    return render(request, 'webside/showmap.html', {'loans': loans, 'communities': communities,})

def loan_delete(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    loan.delete()
    return redirect('loans')

def request_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('requests')

def contact(request):
    text = ""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            text = "Takk for at du tok kontakt!"
            return render(request, 'webside/contact.html', {"text": text})
    else:
        form = ContactForm()
    form.fields['issue_alternative'].label = "Velg et alternativ"
    form.fields['issue_text'].label = "Tekst"
    return render(request, 'webside/contact.html', {'form': form, 'text': text})

def highscore(request):
    users = User.objects.order_by('-profile__sumkarma')[:10]
    if request.method == "POST":
        form = Highscore(request.POST)
        if form.is_valid():
            users=User.objects.filter(profile__community=request.POST.get('community')).order_by('-profile__sumkarma')[:10]
            return render(request, 'webside/highscore.html', {'form' : form, 'users' : users})
    else:
        form=Highscore()
    form.fields['community'].label = "Velg område for å se highscore for valgte område"
    return render(request, 'webside/highscore.html', {'form' : form, 'users' : users})

@login_required
def profile_edit(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()  # you can just save the form, it will save the profile
            return redirect('profile')

    else:  # GET
        form = ProfileUpdateForm(instance=user.profile) # initialise with instance
    form.fields['birth_date'].label = "Fødselsdato"
    form.fields['community'].label = "Velg nytt område"

    context = {
        'form' : form
    }
    return render(request, 'webside/profile_edit.html', context)

@login_required
def profile(request):
    return render(request, 'webside/profile.html')

def statistics(request):
    return render( request, 'webside/statistics.html')

def statisticsUsers(request):
    all_users = User.objects.all().count()
    all_women = User.objects.filter(profile__gender = "kvinne").count()
    all_men = User.objects.filter(profile__gender = "mann").count()
    all_else = User.objects.filter(profile__gender = "annet").count()
    week_1 = timezone.now().date() - timezone.timedelta(days=7)
    week_2 = timezone.now().date() - timezone.timedelta(days=14)
    week_3 = timezone.now().date() - timezone.timedelta(days=21)
    week_4 = timezone.now().date() - timezone.timedelta(days=28)
    week_5 = timezone.now().date() - timezone.timedelta(days=35)
    week_1users = User.objects.filter(date_joined__gte = week_1, date_joined__lte = timezone.now().date() + timezone.timedelta(days=1)).count()
    week_2users = User.objects.filter(date_joined__gte = week_2, date_joined__lte = week_1).count()
    week_3users = User.objects.filter(date_joined__gte = week_3, date_joined__lte = week_2).count()
    week_4users = User.objects.filter(date_joined__gte = week_4, date_joined__lte = week_3).count()
    week_5users = User.objects.filter(date_joined__gte = week_5, date_joined__lte = week_4).count()
    if request.method == "POST":
        form = StatisticsUsersForm(request.POST)
        if request.POST.get('gender') != 'alle' and request.POST.get('community') == "":
            all_0_19 = User.objects.filter(profile__age__gte = 0, profile__age__lte = 19, profile__gender = request.POST.get('gender')).count()
            all_20_29 = User.objects.filter(profile__age__gte = 20, profile__age__lte = 29, profile__gender = request.POST.get('gender')).count()
            all_30_39 = User.objects.filter(profile__age__gte = 30, profile__age__lte = 39, profile__gender = request.POST.get('gender')).count()
            all_40_49 = User.objects.filter(profile__age__gte = 40, profile__age__lte = 49, profile__gender = request.POST.get('gender')).count()
            all_50_59 = User.objects.filter(profile__age__gte = 50, profile__age__lte = 59, profile__gender = request.POST.get('gender')).count()
            all_60_69 = User.objects.filter(profile__age__gte = 60, profile__age__lte = 69, profile__gender = request.POST.get('gender')).count()
            all_70 = User.objects.filter(profile__age__gte = 70, profile__age__lte = 150, profile__gender = request.POST.get('gender')).count()
        elif request.POST.get('gender') == 'alle' and request.POST.get('community') != "":
            all_0_19 = User.objects.filter(profile__age__gte = 0, profile__age__lte = 19, profile__community__name = request.POST.get('community')).count()
            all_20_29 = User.objects.filter(profile__age__gte = 20, profile__age__lte = 29, profile__community__name = request.POST.get('community')).count()
            all_30_39 = User.objects.filter(profile__age__gte = 30, profile__age__lte = 39, profile__community__name = request.POST.get('community')).count()
            all_40_49 = User.objects.filter(profile__age__gte = 40, profile__age__lte = 49, profile__community__name = request.POST.get('community')).count()
            all_50_59 = User.objects.filter(profile__age__gte = 50, profile__age__lte = 59, profile__community__name = request.POST.get('community')).count()
            all_60_69 = User.objects.filter(profile__age__gte = 60, profile__age__lte = 69, profile__community__name = request.POST.get('community')).count()
            all_70 = User.objects.filter(profile__age__gte = 70, profile__age__lte = 150, profile__community__name = request.POST.get('community')).count()
        elif request.POST.get('gender') != 'alle' and request.POST.get('community') != "":
            all_0_19 = User.objects.filter(profile__age__gte = 0, profile__age__lte = 19, profile__gender = request.POST.get('gender'), profile__community__name = request.POST.get('community')).count()
            all_20_29 = User.objects.filter(profile__age__gte = 20, profile__age__lte = 29, profile__gender = request.POST.get('gender'), profile__community__name = request.POST.get('community')).count()
            all_30_39 = User.objects.filter(profile__age__gte = 30, profile__age__lte = 39, profile__gender = request.POST.get('gender'), profile__community__name = request.POST.get('community')).count()
            all_40_49 = User.objects.filter(profile__age__gte = 40, profile__age__lte = 49, profile__gender = request.POST.get('gender'), profile__community__name = request.POST.get('community')).count()
            all_50_59 = User.objects.filter(profile__age__gte = 50, profile__age__lte = 59, profile__gender = request.POST.get('gender'), profile__community__name = request.POST.get('community')).count()
            all_60_69 = User.objects.filter(profile__age__gte = 60, profile__age__lte = 69, profile__gender = request.POST.get('gender'), profile__community__name = request.POST.get('community')).count()
            all_70 = User.objects.filter(profile__age__gte = 70, profile__age__lte = 150, profile__gender = request.POST.get('gender'), profile__community__name = request.POST.get('community')).count()
        else:
            all_0_19 = User.objects.filter(profile__age__gte = 0, profile__age__lte = 19).count()
            all_20_29 = User.objects.filter(profile__age__gte = 20, profile__age__lte = 29).count()
            all_30_39 = User.objects.filter(profile__age__gte = 30, profile__age__lte = 39).count()
            all_40_49 = User.objects.filter(profile__age__gte = 40, profile__age__lte = 49).count()
            all_50_59 = User.objects.filter(profile__age__gte = 50, profile__age__lte = 59).count()
            all_60_69 = User.objects.filter(profile__age__gte = 60, profile__age__lte = 69).count()
            all_70 = User.objects.filter(profile__age__gte = 70, profile__age__lte = 150).count()
    else:
        all_0_19 = User.objects.filter(profile__age__gte = 0, profile__age__lte = 19).count()
        all_20_29 = User.objects.filter(profile__age__gte = 20, profile__age__lte = 29).count()
        all_30_39 = User.objects.filter(profile__age__gte = 30, profile__age__lte = 39).count()
        all_40_49 = User.objects.filter(profile__age__gte = 40, profile__age__lte = 49).count()
        all_50_59 = User.objects.filter(profile__age__gte = 50, profile__age__lte = 59).count()
        all_60_69 = User.objects.filter(profile__age__gte = 60, profile__age__lte = 69).count()
        all_70 = User.objects.filter(profile__age__gte = 70, profile__age__lte = 150).count()
    form = StatisticsUsersForm()
    form.fields['gender'].label = "Kjønn"
    form.fields['community'].label = "Område"
    return render( request, 'webside/statistics_users.html', {'form': form, 'week_1users': week_1users, 'week_2users': week_2users, 'week_3users': week_3users, 'week_4users': week_4users, 'week_5users': week_5users, 'all_users': all_users, 'all_women': all_women, 'all_men': all_men, 'all_else':all_else, 'all_0_19':all_0_19, 'all_20_29':all_20_29, 'all_30_39':all_30_39, 'all_40_49':all_40_49, 'all_50_59':all_50_59, 'all_60_69':all_60_69, 'all_70':all_70 })

def statisticsTrades(request):

    all_trades = Trade_request.objects.all().count() + Trade_loan.objects.all().count()
    last_week = timezone.now().date() - timezone.timedelta(days=7)
    last_mounth = timezone.now().date() - timezone.timedelta(days=30)
    last_6mounth = timezone.now().date() - timezone.timedelta(days=182)
    last_year = timezone.now().date() - timezone.timedelta(days=365)
    last_week_trades = Trade_request.objects.filter(created_date__gte = last_week, created_date__lte = timezone.now().date() + timezone.timedelta(days=1)).count() + Trade_loan.objects.filter(created_date__gte = last_week, created_date__lte = timezone.now().date() + timezone.timedelta(days=1)).count()
    last_mounth_trades = Trade_request.objects.filter(created_date__gte = last_mounth, created_date__lte = timezone.now().date() + timezone.timedelta(days=1)).count() + Trade_loan.objects.filter(created_date__gte = last_mounth, created_date__lte = timezone.now().date() + timezone.timedelta(days=1)).count()
    last_6mounth_trades = Trade_request.objects.filter(created_date__gte = last_6mounth, created_date__lte = timezone.now().date() + timezone.timedelta(days=1)).count() + Trade_loan.objects.filter(created_date__gte = last_mounth, created_date__lte = timezone.now().date() + timezone.timedelta(days=1)).count()
    last_year_trades = Trade_request.objects.filter(created_date__gte = last_year, created_date__lte = timezone.now().date() + timezone.timedelta(days=1)).count() + Trade_loan.objects.filter(created_date__gte = last_year, created_date__lte = timezone.now().date() + timezone.timedelta(days=1)).count()

    week_1 = timezone.now().date() - timezone.timedelta(days=7)
    week_2 = timezone.now().date() - timezone.timedelta(days=14)
    week_3 = timezone.now().date() - timezone.timedelta(days=21)
    week_4 = timezone.now().date() - timezone.timedelta(days=28)
    week_5 = timezone.now().date() - timezone.timedelta(days=35)
    week_1trades = Trade_request.objects.filter(created_date__gte = week_1, created_date__lte = timezone.now().date() + timezone.timedelta(days=1)).count() + Trade_loan.objects.filter(created_date__gte = week_1, created_date__lte = timezone.now().date() + timezone.timedelta(days=1)).count()
    week_2trades = Trade_request.objects.filter(created_date__gte = week_2, created_date__lte = week_1).count() + Trade_loan.objects.filter(created_date__gte = week_2, created_date__lte = week_1).count()
    week_3trades = Trade_request.objects.filter(created_date__gte = week_3, created_date__lte = week_2).count() + Trade_loan.objects.filter(created_date__gte = week_3, created_date__lte = week_2).count()
    week_4trades = Trade_request.objects.filter(created_date__gte = week_4, created_date__lte = week_3).count() + Trade_loan.objects.filter(created_date__gte = week_4, created_date__lte = week_3).count()
    week_5trades = Trade_request.objects.filter(created_date__gte = week_5, created_date__lte = week_4).count() + Trade_loan.objects.filter(created_date__gte = week_5, created_date__lte = week_4).count()

    other = Trade_request.objects.filter(post__category = "annet").count() + Trade_loan.objects.filter(loan__category = "annet").count()
    medical = Trade_request.objects.filter(post__category = "legemiddel").count() + Trade_loan.objects.filter(loan__category = "legemiddel").count()
    school = Trade_request.objects.filter(post__category = "skole").count() + Trade_loan.objects.filter(loan__category = "skole").count()
    little_things = Trade_request.objects.filter(post__category = "småting").count() + Trade_loan.objects.filter(loan__category = "småting").count()

    trades = ""
    if request.method == "POST":
        form = StatisticsUsersForm(request.POST)
        if request.POST.get('gender') != 'alle' and request.POST.get('community') == "" and request.POST.get('category') == "annet":
            print('gender')
            trades = Trade_request.objects.filter(giver__profile__gender = request.POST.get('gender')).count() + Trade_request.objects.filter(receiver__profile__gender = request.POST.get('gender')).count() + Trade_loan.objects.filter(giver__profile__gender = request.POST.get('gender')).count() + Trade_loan.objects.filter(receiver__profile__gender = request.POST.get('gender')).count()
        elif request.POST.get('gender') == 'alle' and request.POST.get('community') != "" and request.POST.get('category') == "annet":
            trades = Trade_request.objects.filter(post__community__name = request.POST.get('community')).count() + Trade_loan.objects.filter(loan__community__name = request.POST.get('community')).count()
        elif request.POST.get('gender') == 'alle' and request.POST.get('community') == "" and request.POST.get('category') != "annet":
            trades = Trade_request.objects.filter(post__category = request.POST.get('category')).count() + Trade_loan.objects.filter(loan__category = request.POST.get('category')).count()
        elif request.POST.get('gender') != 'alle' and request.POST.get('community') != "" and request.POST.get('category') == "annet":
            trades = Trade_request.objects.filter(giver__profile__gender = request.POST.get('gender'), post__community__name = request.POST.get('community')).count() + Trade_request.objects.filter(receiver__profile__gender = request.POST.get('gender'), post__community__name = request.POST.get('community')).count() + Trade_loan.objects.filter(giver__profile__gender = request.POST.get('gender'), loan__community__name = request.POST.get('community')).count() + Trade_loan.objects.filter(receiver__profile__gender = request.POST.get('gender'), loan__community__name = request.POST.get('community')).count()
        elif request.POST.get('gender') != 'alle' and request.POST.get('community') == "" and request.POST.get('category') != "annet":
            trades = Trade_request.objects.filter(giver__profile__gender = request.POST.get('gender'), post__category = request.POST.get('category')).count() + Trade_request.objects.filter(receiver__profile__gender = request.POST.get('gender'), post__category = request.POST.get('category')).count() + Trade_loan.objects.filter(giver__profile__gender = request.POST.get('gender'), loan__category = request.POST.get('category')).count() + Trade_loan.objects.filter(receiver__profile__gender = request.POST.get('gender'), loan__category = request.POST.get('category')).count()
        elif request.POST.get('gender') == 'alle' and request.POST.get('community') != "" and request.POST.get('category') != "annet":
            trades = Trade_request.objects.filter(post__category = request.POST.get('category'), post__community__name = request.POST.get('community')).count() + Trade_loan.objects.filter(loan__category = request.POST.get('category'), loan__community__name = request.POST.get('community')).count()
        elif request.POST.get('gender') != 'alle' and request.POST.get('community') != "" and request.POST.get('category') != "annet":
            trades = Trade_request.objects.filter(giver__profile__gender = request.POST.get('gender'), post__community__name = request.POST.get('community'), post__category = request.POST.get('category')).count() + Trade_request.objects.filter(receiver__profile__gender = request.POST.get('gender'), post__community__name = request.POST.get('community'), post__category = request.POST.get('category')).count() + Trade_loan.objects.filter(giver__profile__gender = request.POST.get('gender'), loan__community__name = request.POST.get('community'), loan__category = request.POST.get('category')).count() + Trade_loan.objects.filter(receiver__profile__gender = request.POST.get('gender'), loan__community__name = request.POST.get('community'), loan__category = request.POST.get('category')).count()
        else:
            trades = all_trades
    form = StatisticsTradesForm()
    form.fields['gender'].label = "Kjønn"
    form.fields['community'].label = "Område"
    form.fields['category'].label = "Kategori"
    return render( request, 'webside/statistics_trades.html', {'form': form, 'all_trades': all_trades, 'last_week_trades': last_week_trades, 'last_mounth_trades': last_mounth_trades, 'last_6mounth_trades': last_6mounth_trades, 'last_year_trades': last_year_trades, 'week_1trades': week_1trades, 'week_2trades': week_2trades, 'week_3trades': week_3trades, 'week_4trades': week_4trades, 'week_5trades': week_5trades, 'other': other, 'school': school, 'medical': medical, 'little_things': little_things, 'trades': trades})
