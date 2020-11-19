from django.shortcuts import render
import sqlite3

profiles = [
    {
        'name': 'Andy Pavlo',
        'position': 'Assistant Professor',
        'dept_name': 'Computer Science',
        'qualification': 'PhD'
    }
]


def home(request):
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professor")
    id, name, pos, dept, qual = cursor.fetchone()
    profiles.append({
        'name': name,
        'position': pos,
        'dept_name': dept,
        'qualification': qual
    })
    context = {
        'profiles': profiles
    }
    return render(request, 'home/home.html', context)
