from django.http.response import HttpResponse
from django.shortcuts import render
from django import forms
import sqlite3

def addReview(request, prof_id, course_name):
    if request.method == 'POST':
        form = forms.Form(request.POST)
        if form.is_valid():
            data = form.data
            # form.declared_fields
            return HttpResponse(form.cleaned_data)
    # Fetching professor name
    cursor = sqlite3.connect('./db.sqlite3').cursor()
    cursor.execute("SELECT name FROM professor WHERE prof_id = ?;", (prof_id,))
    prof_name = cursor.fetchone()[0]

    context = {'course_name': course_name, 'prof_name': prof_name}
    return render(request, 'review/add_review.html', context)