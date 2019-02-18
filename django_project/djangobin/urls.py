from django.urls import re_path, include, path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.shortcuts import reverse

from . import views

app_name = 'djangobin'

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<slug:username>/', views.profile, name='profile'),
    path('trending/', views.trending_snippets, name='trending_snippets'),
    path('trending/<slug:language_slug>/', views.trending_snippets, name='trending_snippets'),
    path('<int:snippet_slug>/', views.snippet_detail, name='snippet_detail'),
    path('tag/<slug:tag>', views.tag_list, name='tag_list'),
    path('download/<slug:snippet_slug>', views.download_snippet, name='download_snippet'),
    path('raw/<slug:snippet_slug>', views.raw_snippet, name='raw_snippet'),
    path('contact/', views.contact, name='contact'),

    path('login/', auth_views.LoginView.as_view(template_name="djangobin/login.html"),
        name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='djangobin/logout.html'),
         name='logout'),

    path('userdetails/', views.user_details, name='user_details'),
    path('signup/', views.signup, name='signup'),

    re_path(r'^activate/' r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='djangobin/password_reset.html',
        email_template_name='djangobin/email/password_reset_email.txt',
        subject_template_name='djangobin/email/password_reset_subject.txt',
        success_url=reverse_lazy('djangobin:password_reset_done')),
         name='password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
            template_name='djangobin/password_reset_done.html'),
            name='password_reset_done'),

    re_path(r'^password-confirm/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='djangobin/password_reset_confirm.html',
            success_url=reverse_lazy('djangobin:password_reset_complete')),
            name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
            template_name='djangobin/password_reset_complete.html'),
            name='password_reset_complete'),

    path('settings/', views.settings, name='settings'),
    path('delete/<slug:snippet_slug>', views.delete_snippet, name='delete_snippet'),
]
