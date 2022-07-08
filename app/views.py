from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connection

# Create your views here.
def getlocs(request):
    if request.method != 'GET':
        return HttpResponse(status=404)
    
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM monsterloc;')
    rows = cursor.fetchall()

    response = {}
    response['monsterloc'] = rows # **DUMMY response!**
    return JsonResponse(response)
