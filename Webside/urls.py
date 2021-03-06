from django.urls import path, include
from django.conf.urls import url
from . import views
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.homepage, name='home'),
    path('requests', views.requests, name='requests'),
    path('post/<int:pk>/', views.requests_detail, name='requests_detail'),
    path('requests/new/', views.requests_new, name='requests_new'),
    path('loans', views.loans, name='loans'),
    path(r'loan/<int:pk>/', views.loans_detail, name='loans_detail'),
    path('loans/new/', views.loans_new, name='loans_new'),
    url(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<int:pk>/commentloan/', views.add_comment_to_loan, name='add_comment_to_loan'),
    path('map', views.showmap, name='map'),
    path('add_community', views.add_community, name='add_community'),
    path('communitylist', views.communitylist, name='communitylist'),
    path('showmap', views.showmap, name='showmap'),
    path('request/delete/<int:pk>/', views.request_delete, name='request_delete'),
    path('loan/delete/<int:pk>/', views.loan_delete, name='loan_delete'),
    path('contact', views.contact, name='contact'),
    path('highscore', views.highscore, name='highscore'),
    path('profile', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('statistics', views.statistics, name='statistics'),
    path('statistics_users', views.statisticsUsers, name='statistics_users'),
    path('statistics_trades', views.statisticsTrades, name='statistics_trades'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
