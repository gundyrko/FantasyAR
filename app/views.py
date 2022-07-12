from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import random

# Create your views here.
@csrf_exempt
def getlocs(request):
    lat_limit = 100 
    long_limit = 100 # range limit from user's location
    min_monster_num = 5 # minimum monster number
    max_monster_num = 10 # maximum monster number

    if request.method == 'POST':
        json_data = json.loads(request.body)
        user_latitude = float(json_data['latitude'])
        user_longitude = float(json_data['longitude'])
        
        # Get all monsters' locations from database
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM monsterloc;')
        rows = cursor.fetchall()
        
        # Get monsters' info in the limit range
        chosen_monster = []
        for row in rows:
            monster_lat = float(row[1])
            monster_long = float(row[2])
            if abs(monster_lat - user_latitude) < lat_limit and abs(monster_long- user_longitude) < long_limit:
                chosen_monster.append(row)
        
        # Generate new monsters' info if needed
        num_monster = len(chosen_monster)
        new_monster_num = 0
        if num_monster < min_monster_num:
            new_monster_num = random.randint(min_monster_num - num_monster, max_monster_num - num_monster)
            for i in range(new_monster_num):
                new_monster = []
                new_id = -1
                new_lat = random.uniform(user_latitude - lat_limit, user_latitude + lat_limit)
                new_long = random.uniform(user_longitude - long_limit, user_longitude + long_limit)
                cursor.execute('INSERT INTO monsterloc (lat, long) VALUES '
                               '(%s, %s);', (new_lat, new_long))
                new_monster.append(new_id)
                new_monster.append(new_lat)
                new_monster.append(new_long)
                chosen_monster.append(new_monster)

        response = {}
        response['monsterloc'] = chosen_monster
        response['userloc'] = {}
        response['userloc']['latitude'] = user_latitude
        response['userloc']['longitude'] = user_longitude
        response['num'] = len(chosen_monster)
        response['new_monster_num'] = new_monster_num
        return JsonResponse(response)

    elif request.method == 'GET':
        # Get all monsters' locations from database
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM monsterloc;')
        rows = cursor.fetchall()
        response = {}
        response['monsterloc'] = rows
        return JsonResponse(response)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def removeloc(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    latitude = json_data['latitude']
    longitude = json_data['longitude']
    cursor = connection.cursor()
    # Remove the monster's location in the database
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
    # Add the monster's location in the database
    cursor.execute('INSERT INTO monsterloc (lat, long) VALUES '
                   '(%s, %s);', (float(latitude), float(longitude)))
    response = {}
    # response['latitude'] = latitude
    # response['longitude'] = longitude
    return JsonResponse(response)