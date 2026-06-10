from django.http import HttpResponse
from django.shortcuts import render

def homePage(request):
    return HttpResponse("Welcome to the Home Page of Student Management System")