from django.conf.urls import url
from .views import index, add_friend, validate_npm, friend_list, get_friend_list
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add-friend/$', add_friend, name='add-friend'),
    url(r'^validate-npm/$', validate_npm, name='validate-npm'),
    url(r'^friend-list/$', friend_list, name='friend-list'),
    url(r'^get-friend-data/$', get_friend_list, name='get-friend-lsit'),
]
