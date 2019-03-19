from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_google_maps import fields as map_fields


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    community = models.ForeignKey('Webside.Community', on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    given = models.IntegerField(default=0)
    gotten = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Comment(models.Model):
    post = models.ForeignKey('Webside.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Comment2(models.Model):
    loan = models.ForeignKey('Webside.Loan', on_delete=models.CASCADE, related_name='comments2')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author2')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Loan(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    title = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    community = models.ForeignKey('Webside.Community', on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Community(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    address = map_fields.AddressField(max_length=200)
    longitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)


    def __str__(self):
        return self.name

class Report(models.Model):
    reason = models.TextField()
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'user_reporting')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'user_gets_reported')

    def __str__(self):
        return self.reason

class Trade_request(models.Model):
    rating = models.IntegerField()
    giver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'user_giving', null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'user_get', null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_given')

    def __str__(self):
        return self.post.title

class Trade_loan(models.Model):
    rating = models.IntegerField()
    giver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'user_giver', null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'user_receiver', null=True)
    loan = models.ForeignKey('Webside.Loan', on_delete=models.CASCADE, related_name='loan_given')

    def __str__(self):
        return self.loan.title
