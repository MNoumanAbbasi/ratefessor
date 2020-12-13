from django.shortcuts import render
from django.http import HttpResponseBadRequest
import sqlite3
from .db_helpers import *
# Create your views here.

def executor(request):
    if (request.user.is_superuser):
        # Getting search results
        query = request.GET.get('execute_query')
        if query == "": 
            return HttpResponseBadRequest("Invalid Query")
            
        result = execute_query(query)
        if (result):
            return render(request, 'adminPortals/executor.html', {"results": result} )
        else:
            return HttpResponseBadRequest("Command Executed")
    else:
        return HttpResponseBadRequest("You must be logged in as a superuser to execute queriess")

    #Simply load the page in the case of first visit
