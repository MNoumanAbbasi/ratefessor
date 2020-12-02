from django.shortcuts import render
from django.http import HttpResponseBadRequest
import sqlite3
# Create your views here.

def loading(request):
    query = request.GET.get('search_query')
    prof = request.GET.get('professor')
    course = request.GET.get('course')
    comb = request.GET.get('combined')

    print(query)
    print(prof)
    print(course)
    print(comb)

    if prof == "1" and course == "0" and comb == "0":
        return search_professor(request, query)
    elif course == "1" and prof == "0" and comb == "0":
        return search_course(request, query)
    elif comb == "1" and course == "0" and prof == "0":
        return search_combo(request, query)
    else:
        return HttpResponseBadRequest('Choose one option!')

def search_professor(request, query):
    status = ""
    professor_list = []

    # Getting search results
    # query = request.GET.get('prof_query')
    query = query

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

def search_course(request, query):
    status = ""
    course_list = []

    # Getting search results
    # query = request.GET.get('course_query')
    query = query

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

def search_combo(request, query):
    status = ""
    
    # Getting search results
    # query = request.GET.get('comb_query')
    query = query

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
    #Send the data recieved
    
    context = {
        'status': query,
    }

    return render(request, 'search/search_combo.html', context)