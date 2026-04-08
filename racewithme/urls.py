"""racewithme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, re_path, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from users import views as user_views
from users.forms import MyPasswordResetForm

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    
    # signup
    re_path(r'^signup/$', user_views.signup, name='signup'),
    re_path(r'^account_activation_sent/$', user_views.account_activation_sent,
        name='account_activation_sent'),
    path(r'activate/<uidb64>/<token>/',
        user_views.activate, name='activate'),

    # auth
    re_path(r'^home/$', TemplateView.as_view(template_name='home.html'), name='home'),
    re_path(r'^$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    # password reset
    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(), {'password_reset_form': MyPasswordResetForm}, 
        name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # main app urls
    re_path(r'^main/', include('main.urls')),
]
