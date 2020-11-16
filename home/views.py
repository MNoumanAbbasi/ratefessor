from django.shortcuts import render

profiles = [
    {
        'name': 'Andy Pavlo',
        'position': 'Assistant Professor',
        'dept_name': 'Computer Science',
        'qualification': 'PhD'
    }
]


def home(request):
    context = {
        'profiles': profiles
    }
    return render(request, 'home/home.html', context)
