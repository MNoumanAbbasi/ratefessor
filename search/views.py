from django.shortcuts import render
from django.http import HttpResponseBadRequest
import sqlite3
import numpy as np
from .db_helpers import *
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
    professor_list = []

    # Getting search results
    query = request.GET.get('search_query')
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
    result = get_prof(query)
    professor_list = [{'id': item[0], 'name': item[1], 'position': item[2], 'dept_name': item[3], 'qualification': item[4]} for item in result]

    # TODO: Remove afterwards. Hard coded for testing:
    hard_code = False
    if hard_code:
        professor_list.append({'id': 50, 'name': 'Nouman Abbasi', 'position': 'Department Chair', 'dept_name': 'Computer Science', 'qualification': "Bht kuch"})
        print(professor_list)

    #Sending off data
    context = {
        'status': len(professor_list),
        'professor_list': professor_list
    }

    return render(request, 'search/search_professor.html', context)

def search_course(request):
    course_list = []

    # Getting search results
    query = request.GET.get('search_query')
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
    result = get_course(query)
    course_list = [{'course_name': item[0], 'level': item[1]} for item in result]
    
    context = {
        'status': len(course_list),
        'course_list': course_list
    }

    return render(request, 'search/search_course.html', context)

def filter(request):
    #ONLY because stupid errors and maine engraizi likhni hai huh
    prof = ""
    empty = ""
    level = ""
    #Get data 
    prof_course_query = request.GET.get('prof_course_filter')
    level_query = request.GET.get('level_filter')
    range_query = request.GET.get('range_filter')
    # TODO: Remove afterwards. Printed for testing
    print(prof_course_query)
    print(level_query)
    print(range_query)

    #Could also filter by department

    if (prof is empty):
        if (level is empty):
            if (range is empty):
                #all three are empty and ratings are 0 - give them no results yet page
                context = {
                    'status': 0
                }

                return render(request, 'search/search_combo.html', context)
            else:
                return None
                #only range - return all course + instructor tuples matching those ratings 
                # SELECT professor.prof_id, professor.name, prof_sec.course_name, course.level
                #     FROM prof_sec 
                #     INNER JOIN professor ON prof_sec.prof_id=professor.prof_id 
                #     LEFT JOIN course ON course.course_name = prof_sec.course_name
                #     WHERE (professor.prof_id, prof_sec.course_name) IN (SELECT prof_id, course_name 
                #                                                             FROM reviews WHERE review_id = (SELECT review_id FROM ratings WHERE ...));
        else: #level is not empty
            if (range is empty):
                return None
                #only level - return all course + instructor tuples matching that level
                #same query as get_prof_course_comb but with a WHERE level filter
            else:
                return None
                #only range and level
                # SELECT professor.prof_id, professor.name, prof_sec.course_name, course.level
                #     FROM prof_sec 
                #     INNER JOIN professor ON prof_sec.prof_id=professor.prof_id 
                #     LEFT JOIN course ON course.course_name = prof_sec.course_name
                #     WHERE course.level = ? AND (professor.prof_id, prof_sec.course_name) IN (SELECT prof_id, course_name 
                #                                                             FROM reviews WHERE review_id = (SELECT review_id FROM ratings WHERE ...));
    else: #the branch where prof is not empty
        if (level is empty):
            if (range is empty):
                return None
                #only text - simply return all course + instructor tuples matching that text
                #simply call get_prof_course_comb
            else:
                return None
                #only text and range
                #Add the nested query for range next to the last line in get_prof_course_comb
        else: #level is not empty
            if (range is empty):
                return None
                #text and level
                #simply add an 'AND level = ?' in get_prof_course_comb
            else:
                return None
                #text, level and range
                #For a particular course+instructor tuple, filter it through range and level 

    #Send the data recieved 
    context = {
        'status': 0
    }

    return render(request, 'search/search_combo.html', context)

def search_combo(request):
    comb_list = []

    # Getting search results from homepage
    query = request.GET.get('search_query')
    # TODO: Remove afterwards. Printed for testing
    print(query)

    #Getting search results from the search_combo page
    if query is None:
        query = request.GET.get('comb_query')
        # TODO: Remove afterwards. Printed for testing
        print("From comb: ", query)

    #Display zero results in the case of an empty query
    if query == None or query == "" or query == "\n": 
        context = {
            'status': "No query",
        }
        return render(request, 'search/search_combo.html', context)
    
    result_comb = get_prof_course_comb(query)

    #for each pair - get the ratings if any 
    for row in result_comb:
        #getting the ratings
        rating_tuple = get_ratings(row[0], row[2])
        if rating_tuple is not None:
            ratings = np.array(rating_tuple)
            cum_ratings = np.round(np.mean(ratings, axis = 0, dtype = np.float64), 2)
        else:
            cum_ratings = [-1]
        comb_list.append({'prof_id': row[0], 'prof_name': row[1], 'course_name': row[2], 'level': row[3], 'ratings': cum_ratings})
    
    #Send the data recieved    
    context = {
        'status': len(comb_list),
        'combined_list': comb_list
    }

    return render(request, 'search/search_combo.html', context)