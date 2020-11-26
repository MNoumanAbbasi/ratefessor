from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='app-home'),
    path('professor/<id>', views.professor, name='professor-profile'),
    path('course/<course_name>', views.course, name='course-profile'),
]