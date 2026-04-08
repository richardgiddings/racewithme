from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^user_settings/', views.user_settings, name='user_settings'),
    re_path(r'^user_profile/', views.user_profile, name='user_profile'),
    re_path(r'^races/', views.races, name='races'),
    re_path(r'^interested/', views.interested, name='interested'),
    re_path(r'^going/', views.going, name='going'),
    re_path(r'^no_longer_interested/', views.no_longer_interested, name='no_longer_interested'),
    re_path(r'^no_longer_going/', views.no_longer_going, name='no_longer_going'),
    re_path(r'^completed/', views.completed, name='completed'),
    re_path(r'^set_target_time', views.set_target_time, name='set_target_time'),
    re_path(r'^completed_race/(?P<id>\d+)$', views.completed_race, name='completed_race'),
    re_path(r'^results_form', views.results_form, name='results_form'),
    re_path(r'^friends/', views.friends, name='friends'),
    re_path(r'^add_friend/', views.add_friend, name='add_friend'),
    re_path(r'^friend_details/(?P<id>\d+)$', views.friend_details, name='friend_details'),
    re_path(r'^remove_friend/', views.remove_friend, name='remove_friend'),
    re_path(r'^suggest_race/', views.suggest_race, name='suggest_race'),

    # email queues
    re_path(r'^django-rq/', include('django_rq.urls')),
]