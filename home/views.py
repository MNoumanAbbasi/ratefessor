from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    if (request.user.is_superuser):
        return render(request, 'home/home_admin.html')
    else:
        return render(request, 'home/home.html')

@login_required(login_url="/accounts/signin/")
def home_review(request):
    return render(request, 'home/review.html')

