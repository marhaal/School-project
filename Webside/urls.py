from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.homepage, name='home'),
    path('requests', views.requests, name='requests'),
    path('post/<int:pk>/', views.requests_detail, name='requests_detail'),
    path('requests/new/', views.requests_new, name='requests_new'),
]
