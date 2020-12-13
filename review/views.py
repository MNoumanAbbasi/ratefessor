from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import AddReviewForm
from profiles.db_helpers import get_prof_details
from review.db_helpers import add_review, delete_review, get_user_review, vote_review


def addReview(request, prof_id, course_name):

    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            add_review(request.user.id, course_name, prof_id, form.cleaned_data)
            return redirect("combo-profile", prof_id, course_name)
    else:
        user_review = {}
        # Get prefilled form data if user review already exists in DB
        if request.user.is_authenticated:
            user_review = get_user_review(request.user.id, prof_id, course_name)

        if user_review:
            form = AddReviewForm(user_review)
        else:
            form = AddReviewForm()

    prof_name = get_prof_details(prof_id)[1]

    context = {
        'course_name': course_name,
        'prof_name': prof_name,
        'prof_id': prof_id,
        'form': form
    }
    return render(request, 'review/add_review.html', context)


def deleteReview(request, review_id, prof_id, course_name):
    delete_review(review_id, request.user.id)
    return redirect("combo-profile", prof_id, course_name)


def voteReview(request, review_id, vote, prof_id, course_name):
    vote_review(review_id, request.user.id, vote)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect("combo-profile", prof_id, course_name)
