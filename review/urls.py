from django.urls import path
from . import views

urlpatterns = [
    path('<prof_id>/<course_name>', views.addReview, name='add-review'),
]