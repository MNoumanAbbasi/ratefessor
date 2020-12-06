from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .db_helpers import (
    get_course_info, get_courses_of_prof,
    get_prof_details,
    get_profs_of_course,
    get_reviews_ratings
)


def professor(request, id):
    row = get_prof_details(id)

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
    courses = get_courses_of_prof(id)

    # # TODO: Remove afterwards. Hard coded for testing:
    # courses.append({'name': 'Intro. to Programming', 'semester': 'Fall', 'year': 2019})
    # courses.append({'name': 'Intro. to Programming', 'semester': 'Fall', 'year': 2019})
    # courses.append({'name': 'Databases', 'semester': 'Fall', 'year': 2019})
    # courses.append({'name': 'Intro. to Computer Science', 'semester': 'Fall', 'year': 2019})
    # courses.append({'name': 'Probability', 'semester': 'Fall', 'year': 2019})

    # Fetching reviews for this professor
    reviews, avgs = get_reviews_ratings(prof_id=id)

    # TODO: Remove afterwards. Hard coded for testing:
    # reviews.append({'user_id': 1, 'text': 'Very good instructor. Recommended',
    #                 'date': '2020-10-2', 'course_name': 'Intro. to Programming',
    #                 'semester': 'Fall', 'year': 2019})

    context = {
        'professor': professor,
        'courses': courses,
        'reviews': reviews,
        'num_reviews': len(reviews),
        'avgs': avgs
    }

    return render(request, 'profiles/professor.html', context)


def course(request, course_name):
    c = get_course_info(course_name)

    # If no course found
    if c is None:
        return HttpResponseBadRequest('No course found!')
    course = {
        'course_name': c[0],
        'level': c[1]
    }

    # Now fetching all the professors that offered this course
    professors = get_profs_of_course(course_name)

    # Calculating averages
    _, avgs = get_reviews_ratings(course_name=course_name)

    context = {
        'professors': professors,
        'course': course,
        'avgs': avgs
    }

    return render(request, 'profiles/course.html', context)


def combo(request, prof_id, course_name):
    # Fetching course from DB
    reviews, avgs = get_reviews_ratings(prof_id, course_name)
    prof_name = get_prof_details(prof_id)[1]

    context = {
        'reviews': reviews,
        'num_reviews': len(reviews),
        'prof_name': prof_name,
        'prof_id': prof_id,
        'course_name': course_name,
        'avgs': avgs
    }

    return render(request, 'profiles/combo.html', context)
