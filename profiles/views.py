from django.shortcuts import render
from django.http import HttpResponseBadRequest
import sqlite3


def professor(request, id):
    # Fetching professor from DB
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professor WHERE prof_id = ?;", (id,))
    row = cursor.fetchone()

    # If no professor found with that id
    if row is None:
        return HttpResponseBadRequest('No professor found!')
    else:
        context = {
            'id': row[0],
            'name': row[1],
            'position': row[2],
            'dept_name': row[3],
            'qualification': row[4]
        }
        return render(request, 'profiles/professor.html', context)


def course(request, course_name):
    # Fetching course from DB
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM course WHERE course_name = ?;", (course_name,))
    row = cursor.fetchone()

    # If no professor found with that id
    if row is None:
        return HttpResponseBadRequest('No course found!')
    else:
        context = {
            'course_name': row[0],
            'level': row[1]
        }
        return render(request, 'profiles/course.html', context)


def combo(request):
    return render(request, 'profiles/combo.html')
