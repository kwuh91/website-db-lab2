from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db import connection, connections, DatabaseError, IntegrityError, OperationalError
from typing import Any
from django.core.management.base import BaseCommand
from .models import InputHistory
from django.utils import timezone

# Create your views here.

def index(request):
    return render(request, 'playground/authentication.html')

def process_form(request):
    error_msg = "No errors detected"
    history_entries = InputHistory.objects.all()
    if request.method == 'POST':
        # Get the values from the form
        address = request.POST.get('address')
        db_name = request.POST.get('db')
        login = request.POST.get('login')
        pswd = request.POST.get('pswd')
        port = request.POST.get('port')

        # connecting to the database
        connection.settings_dict['HOST'] = address
        connection.settings_dict['NAME'] = db_name
        connection.settings_dict['USER'] = login
        connection.settings_dict['PASSWORD'] = pswd
        connection.settings_dict['PORT'] = port


        # For testing purposes, printing the values
        # print(f"Address: {connection.settings_dict['HOST']}, Database: {connection.settings_dict['NAME']}, Login: {connection.settings_dict['USER']}, Password: {connection.settings_dict['PASSWORD']}, Port: {connection.settings_dict['PORT']}")


        with connection.cursor() as tables:
            tables.execute("SHOW FULL TABLES;")
            return render(request, 'playground/workbench.html', {'data' : None, 'tables' : tables, 'error_msg' : error_msg, 'history_entries' : history_entries})
        
    else:
        query = request.GET.get("qinput")
        print(f"Query: {query}")
        
        # Add logic here

        db_Info = connection.mysql_server_info
        print("Connected to MySQL Server version ", db_Info)


        with connection.cursor() as data, connection.cursor() as tables:
            tables.execute("SHOW FULL TABLES;")
            try:
                data.execute(query)
                InputHistory.objects.create(input_text=query, timestamp=timezone.now())
                history_entries = InputHistory.objects.all()
                return render(request, 'playground/workbench.html', {'data' : data, 'tables' : tables, 'error_msg' : error_msg, 'history_entries' : history_entries})
            except Exception as e:
                error_msg = str(e)
                return render(request, 'playground/workbench.html', {'data' : None, 'tables' : tables, 'error_msg' : error_msg, 'history_entries' : history_entries})
