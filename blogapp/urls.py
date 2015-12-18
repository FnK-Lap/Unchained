from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'blogapp'
urlpatterns = [
    # url('^', include('django.contrib.auth.urls')),
    url(r'^login', auth_views.login, name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^register$', views.register, name='register'),

    url(r'^(?P<pk>[0-9]+)/', views.ShowView.as_view(), name='show'),

    url(r'^(?P<post_id>[0-9]+)/addComment', views.addComment, name='addComment'),

    url(r'^newPost$', views.newPost, name='newPost'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]