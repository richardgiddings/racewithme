from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user_profile/', views.user_profile, name='user_profile'),
    url(r'^races/', views.races, name='races'),
    url(r'^interested/', views.interested, name='interested'),
    url(r'^going/', views.going, name='going'),
]