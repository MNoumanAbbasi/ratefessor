from django.urls import path
from . import views

urlpatterns = [
    path('professor/<id>', views.professor, name='professor-profile'),
    path('course/<course_name>', views.course, name='course-profile'),
    path('combo/<prof_id>/<course_name>', views.combo, name='combo-profile'),
]