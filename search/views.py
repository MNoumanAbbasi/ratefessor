from django.shortcuts import render
from django.http import HttpResponseBadRequest
import sqlite3
import numpy as np
# Create your views here.

def loading(request):
    prof = request.GET.get('professor')
    course = request.GET.get('course')
    comb = request.GET.get('combined')

    print(prof)
    print(course)
    print(comb)

    if prof == "1" and course == "0" and comb == "0":
        return search_professor(request)
    elif course == "1" and prof == "0" and comb == "0":
        return search_course(request)
    elif comb == "1" and course == "0" and prof == "0":
        return search_combo(request)
    else:
        return HttpResponseBadRequest('Choose one option!')

def search_professor(request):
    status = ""
    professor_list = []

    # Getting search results
    query = request.GET.get('search_query')
    # query = query

    # TODO: Remove afterwards. Printed for testing
    print(query)

    #Simply load the page in the case of first visit
    if query is None: 
        context = {
            'status': "No query",
            'professor_list': professor_list
        }
        return render(request, 'search/search_professor.html', context)

    #Fetching professor from DB acc to query
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professor WHERE name = ?;", (query,))
    professor_list = [{'id': item[0], 'name': item[1], 'position': item[2], 'dept_name': item[3], 'qualification': item[4]} for item in cursor.fetchall()]
    if professor_list == []: status = "Not found"
    else: status = len(professor_list)

    # TODO: Remove afterwards. Hard coded for testing:
    hard_code = False
    if hard_code:
        professor_list.append({'id': 50, 'name': 'Nouman Abbasi', 'position': 'Department Chair', 'dept_name': 'Computer Science', 'qualification': "Bht kuch"})
        print(professor_list)
        status = len(professor_list)

    #Sending off data
    context = {
        'status': status,
        'professor_list': professor_list
    }

    return render(request, 'search/search_professor.html', context)

def search_course(request):
    status = ""
    course_list = []

    # Getting search results
    query = request.GET.get('search_query')
    # query = query

    # TODO: Remove afterwards. Printed for testing
    print(query)

    #Simply load the page in the case of first visit
    if query is None: 
        context = {
            'status': "No query",
            'course_list': course_list
        }
        return render(request, 'search/search_course.html', context)
    
    #Fetching professor from course acc to query - checks for substring
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course WHERE course_name LIKE ?", (f'%{query}%',))
    course_list = [{'course_name': item[0], 'level': item[1]} for item in cursor.fetchall()]
    if course_list == []: status = "Not found"
    else: status = len(course_list)
    print(status)
    
    context = {
        'status': status,
        'course_list': course_list
    }

    return render(request, 'search/search_course.html', context)

def search_combo(request):
    status = ""
    
    # Getting search results
    query = request.GET.get('search_query')
    # query = query
    # TODO: Remove afterwards. Printed for testing
    print(query)

    #Simply load the page in the case of first visit
    if query is None: 
        context = {
            'status': "No query",
        }
        return render(request, 'search/search_combo.html', context)

    # TODO: Remove afterwards. Printed for testing
    print(status)

    #Query DB according to filters results and the comb_query
    #SELECT * FROM prof_sec INNER JOIN professor ON prof_sec.prof_id=professor.prof_id WHERE professor.name = 'Algebra' OR prof_sec.course_name LIKE 'Algebra'
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    #Getting all the instructor + course pairs matching the query
    cursor.execute("""SELECT professor.prof_id, professor.name, prof_sec.course_name, course.level
                        FROM prof_sec 
                        INNER JOIN professor ON prof_sec.prof_id=professor.prof_id 
                        LEFT JOIN course ON course.course_name = prof_sec.course_name
                        WHERE professor.name LIKE ? OR prof_sec.course_name LIKE ?;"""
                    , (f'%{query}%', f'%{query}%',))
    # comb_list = [{'prof_id': item[0], 'prof_name': item[1], 'course_name': item[2], 'level': item[3], 'ratings': []} for item in cursor.fetchall()]

    comb_list = []
    #for each pair - get the ratings if any 
    for row in cursor.fetchall():
        #getting the ratings
        cursor.execute("""SELECT rating.workload, rating.learning, rating.grading
                            FROM review
                            INNER JOIN rating ON review.review_id = rating.review_id
                            WHERE review.prof_id = ? AND course_name = ?""", (row[0], row[2]))
        ratings = np.array(cursor.fetchall())
        cum_ratings = np.mean(ratings, axis = 0, dtype = np.float64)
        comb_list.append({'prof_id': row[0], 'prof_name': row[1], 'course_name': row[2], 'level': row[3], 'ratings': cum_ratings})
    
    #Send the data recieved    
    context = {
        'status': len(comb_list),
        'combined_list': comb_list
    }

    return render(request, 'search/search_combo.html', context)