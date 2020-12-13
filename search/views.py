from django.shortcuts import render
from django.http import HttpResponseBadRequest
import sqlite3
from .db_helpers import *
# Create your views here.

def loading(request):
    options = request.GET.get('option')

    print(options)

    if options == "prof":
        return search_professor(request)
    elif options == "course":
        return search_course(request)
    elif options == "comb":
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
    if query == "": 
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
    if query == "": 
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
    #Get data 
    prof_course_query = request.POST.get('prof_course_filter')
    level_query = request.POST.get('level_filter')
    workload_start = request.POST.get('work_start')
    workload_end = request.POST.get('work_end')
    grad_start = request.POST.get('grad_start')
    grad_end = request.POST.get('grad_end')
    learn_start = request.POST.get('learn_start')
    learn_end = request.POST.get('learn_end')
    rating = [float(workload_start), float(workload_end), float(learn_start), float(learn_end), float(grad_start), float(grad_end)]

    # TODO: Remove afterwards. Printed for testing
    print(prof_course_query)
    print(level_query)
    print(workload_start, workload_end)
    print(grad_start, grad_end)
    print(learn_start, learn_end)
    
    query_list = []
    combo_list = []
    no_query = False

    if (prof_course_query == "None"):
        if (level_query == None):
            if (not (any(rating) > 0)):
                #nothing
                query_list = []
                no_query = True
            else:
                #only range - return all course + instructor tuples matching those ratings 
                query_list = filter_acc_ratings(rating)
                print(query_list)
        else:
            if (workload_end == "0" and workload_start == "0"):
                #only level
                query_list = filter_acc_level(level_query)
                print(query_list)
            else: 
                #only range and level
                query_list = filter_acc_level_ratings(level_query, rating)
                print(query_list)
    else: #the branch where prof is not empty
        if (level_query == None):
            if (workload_start == "0" and workload_end == "0"):
                #only text - simply return all course + instructor tuples matching that text
                query_list = get_prof_course_comb(prof_course_query)
                print(query_list)
            else:
                #only text and range
                query_list = filter_acc_prof_course_ratings(prof_course_query, rating)
                print(query_list)
        else: #level is not empty
            if (workload_start == "0" and workload_end == "0"):
                #text and level
                query_list = filter_acc_prof_course_level(prof_course_query, level_query)
                print(query_list)
            else:
                #text, level and range 
                query_list = filter_acc_all(prof_course_query, level_query, rating)
                print(query_list)

    combo_list = get_cards(query_list)

    if no_query == True: status = "No query"
    else: status = len(combo_list)

    #Send the data recieved 
    context = {
        'status': status,
        'combined_list': combo_list
    }

    return render(request, 'search/search_combo.html', context)

def search_combo(request):
    combo_list = []

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
    combo_list = get_cards(result_comb)
    
    #Send the data recieved    
    context = {
        'status': len(combo_list),
        'combined_list': combo_list
    }

    return render(request, 'search/search_combo.html', context)