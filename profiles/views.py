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
    courses.append({'name': 'Intro. to Programming', 'semester': 'Fall', 'year': 2019})
    courses.append({'name': 'Intro. to Programming', 'semester': 'Fall', 'year': 2019})
    courses.append({'name': 'Databases', 'semester': 'Fall', 'year': 2019})
    courses.append({'name': 'Intro. to Computer Science', 'semester': 'Fall', 'year': 2019})
    courses.append({'name': 'Probability', 'semester': 'Fall', 'year': 2019})

    # Fetching reviews for this professor
    cursor.execute("SELECT * FROM review WHERE prof_id = ?;", (id,))
    reviews = [{'user_id': r[1], 'text': r[2], 'date': r[3], 'course_name': r[5], 'semester': r[6], 'year': r[7]}
               for r in cursor.fetchall()]

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
    cursor.execute("SELECT * FROM course WHERE course_name = ?;", (course_name,))
    row = cursor.fetchone()

    # If no professor found with that id
    if row is None:
        return HttpResponseBadRequest('No course found!')

    course = {
        'course_name': row[0],
        'level': row[1]
    }

    # Now fetching all the professors that offered this course
    cursor.execute("SELECT * FROM prof_sec WHERE course_name = ?;", (course_name,))
    professors = []
    for row in cursor.fetchall():
        prof_id = row[0]
        cursor.execute("SELECT * FROM professor WHERE prof_id = ?;", (prof_id,))
        r = cursor.fetchone()
        if r:
            professors.append({'id': r[0], 'name': r[1], 'position': r[2], 'dept_name': r[3]})

    # Also fetching reviews for this course
    cursor.execute("SELECT AVG(workload), AVG(learning), AVG(grading) FROM review NATURAL JOIN rating WHERE course_name = ?;",
                   (course_name,))
    r = cursor.fetchone()
    avgs = {}
    if r:
        avgs = {'workload':round(r[0],1), 'learning':round(r[1],1), 'grading':round(r[2],1)}
        avgs['overall'] = round(sum(avg for avg in avgs.values()) / len(avgs), 1)

    context = {
        'professors': professors,
        'course': course,
        'avgs': avgs
    }

    return render(request, 'profiles/course.html', context)


def combo(request, prof_id, course_name):
    # Fetching course from DB
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM review NATURAL JOIN rating WHERE prof_id = ? AND course_name = ?;",
                   (prof_id, course_name,))
    rows = cursor.fetchall()

    reviews = [{'review_id': r[0], 'user_id':r[1], 'text':r[2], 'date':r[3], 'semester':r[6], 'year':r[7],
                'workload':r[8], 'learning':r[9], 'grading':r[10]} for r in rows]

    cursor.execute("SELECT name FROM professor WHERE prof_id = ?;", (prof_id))
    prof_name = cursor.fetchone()[0]

    # Calculating averages
    avgs = {}
    if reviews:
        avgs = {
            'workload': round(sum(r['workload'] for r in reviews) / len(reviews), 1),
            'learning': round(sum(r['learning'] for r in reviews) / len(reviews), 1),
            'grading': round(sum(r['grading'] for r in reviews) / len(reviews), 1)
        }
        avgs['overall'] = round(sum(avg for avg in avgs.values()) / len(avgs), 1)

    context = {
        'reviews': reviews,
        'num_reviews': len(reviews),
        'prof_name': prof_name,
        'prof_id': prof_id,
        'course_name': course_name,
        'avgs': avgs
    }

    return render(request, 'profiles/combo.html', context)
