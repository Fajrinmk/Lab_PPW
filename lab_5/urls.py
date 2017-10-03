from django.conf.urls import url
from .views import index, add_todo, delete_todo

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add_todo', add_todo, name='add_todo'),
    url(r'^(?P<object_id>[0-9]+)/delete/$', delete_todo, name='delete_todo')
]
