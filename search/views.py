from django.shortcuts import render

# Create your views here.

def search_professor(request):
    return render(request, 'search/search_professor.html')

def search_course(request):
    return render(request, 'search/search_course.html')

def search_combo(request):
    return render(request, 'search/search_combo.html')