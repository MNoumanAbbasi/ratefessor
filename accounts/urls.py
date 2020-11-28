from django.urls import path, re_path
from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'^signup/$', views.signup_view, name="signup"),
    re_path(r'^signin/$', views.signin_view, name="signin"),
    re_path(r'^signout/$', views.signout_view, name="signout"),
]
