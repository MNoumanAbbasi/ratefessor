from django.urls import path, re_path
from django.contrib import admin
from . import views

# app_name = 'home'

urlpatterns = [
    # path('admin', admin.site.urls),
    path('', views.home, name='app-home'),
    re_path(r'^review/$', views.home_review, name="review"),
    # re_path(r'^signin/$', views.signin_view, name="signin"),
    # re_path(r'^signout/$', views.signout_view, name="signout"),

    # path('signin', views.signin, name='signin'),
    # path('signup', views.signup, name='signup'),

]