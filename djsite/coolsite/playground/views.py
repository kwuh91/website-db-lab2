from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db import connection, connections
from .models import *

# Create your views here.

def index(request):
    return render(request, 'playground/base.html')

def process_form(request):
    if request.method == 'POST':
        # Get the values from the form
        address = request.POST.get('address')
        db_name = request.POST.get('db')
        login = request.POST.get('login')
        pswd = request.POST.get('pswd')
        port = request.POST.get('port')

        # Now you can use these values as needed (e.g., connect to the database)
        connection.settings_dict['HOST'] = address
        connection.settings_dict['NAME'] = db_name
        connection.settings_dict['USER'] = login
        connection.settings_dict['PASSWORD'] = pswd
        connection.settings_dict['PORT'] = port


        # For testing purposes, you can print the values
        print(f"Address: {connection.settings_dict['HOST']}, Database: {connection.settings_dict['NAME']}, Login: {connection.settings_dict['USER']}, Password: {connection.settings_dict['PASSWORD']}, Port: {connection.settings_dict['PORT']}")

        # Add your logic here (e.g., connect to the database)
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT * FROM world.city;")
        #     for item in cursor:
        #         print(*item)

        # For now, return a simple response
        return HttpResponse("Form submitted successfully.")
    else:
        return HttpResponse("Form submission failed.")
