from django.urls import path
from . import views

urlpatterns = [
    path('search_professor', views.search_professor, name='search-professor'),
    path('search_course', views.search_course, name='search-course'),
    path('search_professor_course', views.search_combo, name='search-combo'),
]