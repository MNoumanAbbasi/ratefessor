from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django import forms
from .forms import AddReviewForm
import sqlite3
from datetime import datetime


def addReview(request, prof_id, course_name):
    # Fetching professor name
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['semester']
            year = form.cleaned_data['year']
            workload = form.cleaned_data['workload']
            learning = form.cleaned_data['learning']
            grading = form.cleaned_data['grading']
            review = form.cleaned_data['review']

            user_id = request.user.id
            date = datetime.today().strftime('%Y-%m-%d')
            
            cursor.execute("INSERT INTO review (user_id,text,date,prof_id,course_name,semester,year) VALUES (?,?,?,?,?,?,?)",
                           (user_id, review, date, prof_id, course_name, semester, year))
            review_id = cursor.lastrowid
            cursor.execute("INSERT INTO rating VALUES (?,?,?,?)", (review_id, workload, learning, grading))
            conn.commit()
            cursor.close()
            return redirect("combo-profile", prof_id, course_name)
    else:
        form = AddReviewForm()

    cursor.execute("SELECT name FROM professor WHERE prof_id = ?;", (prof_id,))
    prof_name = cursor.fetchone()[0]

    context = {'course_name': course_name, 'prof_name': prof_name, 'form': form}
    return render(request, 'review/add_review.html', context)
