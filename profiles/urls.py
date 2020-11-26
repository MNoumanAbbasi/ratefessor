from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='app-home'),
    path('professor/<id>', views.professor, name='professor-profile'),
    path('course/<id>', views.course, name='course-profile'),
]