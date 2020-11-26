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

    professor = {
        'id': row[0],
        'name': row[1],
        'position': row[2],
        'dept_name': row[3],
        'qualification': row[4]
    }

    # Now fetching all the courses this professor offered
    cursor.execute("SELECT * FROM prof_sec WHERE prof_id = ?;", (id,))
    courses = [{'name': r[1], 'semester': r[2], 'year': r[3]}
               for r in cursor.fetchall()]

    # TODO: Remove afterwards. Hard coded for testing:
    courses.append({'name': 'Intro. to Programming',
                    'semester': 'Fall', 'year': 2019})
    courses.append({'name': 'Intro. to Programming',
                    'semester': 'Fall', 'year': 2019})
    courses.append({'name': 'Databases',
                    'semester': 'Fall', 'year': 2019})
    courses.append({'name': 'Intro. to Computer Science',
                    'semester': 'Fall', 'year': 2019})
    courses.append({'name': 'Probability',
                    'semester': 'Fall', 'year': 2019})

    # Fetching reviews for this professor
    cursor.execute("SELECT * FROM review WHERE prof_id = ?;", (id,))
    reviews = [{'user_id': r[1], 'text': r[2], 'date': r[3], 'course_name': r[5],
                'semester': r[6], 'year': r[7]} for r in cursor.fetchall()]

    # TODO: Remove afterwards. Hard coded for testing:
    reviews.append({'user_id': 1, 'text': 'Very good instructor. Recommended',
                    'date': '2020-10-2', 'course_name': 'Intro. to Programming',
                    'semester': 'Fall', 'year': 2019})

    context = {
        'professor': professor,
        'courses': courses,
        'reviews': reviews
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
