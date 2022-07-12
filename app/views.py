from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json

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


@csrf_exempt
def removeloc(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    latitude = json_data['latitude']
    longitude = json_data['longitude']
    cursor = connection.cursor()
    # cursor.execute('INSERT INTO monsterloc (lat, long) VALUES '
                #    '(%s, %s);', (float(latitude), float(longitude)))
    cursor.execute('DELETE FROM monsterloc WHERE lat = %s AND long = %s;', (float(latitude), float(longitude)))
    response = {}
    # response['latitude'] = latitude
    # response['longitude'] = longitude
    return JsonResponse(response)

@csrf_exempt
def addloc(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    latitude = json_data['latitude']
    longitude = json_data['longitude']
    cursor = connection.cursor()
    cursor.execute('INSERT INTO monsterloc (lat, long) VALUES '
                   '(%s, %s);', (float(latitude), float(longitude)))
    response = {}
    # response['latitude'] = latitude
    # response['longitude'] = longitude
    return JsonResponse(response)