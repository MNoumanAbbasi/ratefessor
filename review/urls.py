from django.urls import path
from . import views

urlpatterns = [
    path('<prof_id>/<course_name>', views.addReview, name='add-review'),
    path('<review_id>/<prof_id>/<course_name>', views.deleteReview, name='delete-review'),
    path('<review_id>/<vote>/<prof_id>/<course_name>', views.voteReview, name='vote-review')
]
