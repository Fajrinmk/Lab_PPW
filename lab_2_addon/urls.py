from django.conf.urls import url
from .views import index_addon
    #url for app
urlpatterns = [
    url(r'^$', index_addon, name='index_addon'),
]
