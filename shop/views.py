from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def plants(request):
    return render(request, 'page1.html')


def about(request):
    return render(request, 'page2.html')


