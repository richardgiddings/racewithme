from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^user_profile/', views.user_profile, name='user_profile'),
    url(r'^races/', views.races, name='races'),
    url(r'^interested/', views.interested, name='interested'),
    url(r'^going/', views.going, name='going'),
    url(r'^no_longer_interested/', views.no_longer_interested, name='no_longer_interested'),
    url(r'^no_longer_going/', views.no_longer_going, name='no_longer_going'),
    url(r'^completed/', views.completed, name='completed'),
    url(r'^set_target_time', views.set_target_time, name='set_target_time'),
    url(r'^completed_race/(?P<id>\d+)$', views.completed_race, name='completed_race'),
    url(r'^results_form', views.results_form, name='results_form'),
    url(r'^friends/', views.friends, name='friends'),
    url(r'^add_friend/', views.add_friend, name='add_friend'),

    # email queues
    url(r'^django-rq/', include('django_rq.urls')),
]