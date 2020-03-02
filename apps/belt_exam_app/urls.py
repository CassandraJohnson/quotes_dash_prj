from django.conf.urls import url, include
from . import views 
urlpatterns = [
    url(r'^$', views.index),
    url(r'^quotes$', views.quotes),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quote$', views.quote_post),
    url(r'^like/(?P<quote_id>\d+)$', views.favorite_quote),
    url(r'^users/(?P<user_id>\d+)$', views.users),
    url(r'^users/edit/(?P<id>\d+)$', views.edit),
    url(r'^users/edit$', views.edit_users),
    url(r'^dashboard$', views.dashboard)
]