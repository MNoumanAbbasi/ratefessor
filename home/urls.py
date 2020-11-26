from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.home, name='app-home'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    
]