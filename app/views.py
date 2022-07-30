from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import random

# Create your views here.
@csrf_exempt
def getlocs(request):
    lat_limit = 0.003
    long_limit = 0.003 # range limit from user's location
    min_lat_limit = 0.0002
    min_long_limit = 0.0002 # minimum difference
    min_monster_num = 5 # minimum monster number
    max_monster_num = 10 # maximum monster number
    num_type = 1 # number of monster types

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
        id_list = []
        for row in rows:
            monster_lat = float(row[1])
            monster_long = float(row[2])
            id_list.append(int(row[0]))
            if abs(monster_lat - user_latitude) < lat_limit and abs(monster_long- user_longitude) < long_limit:
                chosen_monster.append(row)
        
        lat_lower_bound = max(user_latitude - lat_limit, -90)
        lat_upper_bound = min(user_latitude + lat_limit, 90)
        long_lower_bound = max(user_longitude - long_limit, -180)
        long_upper_bound = min(user_longitude + long_limit, 180)
        # Generate new monsters' info if needed
        num_monster = len(chosen_monster)
        new_monster_num = 0
        if num_monster < min_monster_num:
            new_monster_num = random.randint(min_monster_num - num_monster, max_monster_num - num_monster)
            for i in range(new_monster_num):
                new_monster = []
                new_id = -1
                for i in range(65536):
                    if i not in id_list:
                        id_list.append(i)
                        new_id = i
                        break

                new_type = random.randint(0, num_type-1)
                new_lat = 0
                new_long = 0
                while True:
                    well_placed = True
                    new_lat = random.uniform(lat_lower_bound, lat_upper_bound)
                    new_long = random.uniform(long_lower_bound, long_upper_bound)
                    for monster in chosen_monster:
                        if abs(new_lat - monster[1]) < min_lat_limit or abs(new_long - monster[2]) < min_long_limit:
                            well_placed = False
                            break
                    
                    if well_placed:
                        break


                cursor.execute('INSERT INTO monsterloc (id, lat, long, type) VALUES '
                               '(%s, %s, %s, %s);', (new_id, new_lat, new_long, new_type))
                new_monster.append(new_id)
                new_monster.append(new_lat)
                new_monster.append(new_long)
                new_monster.append(new_type)
                chosen_monster.append(new_monster)

        response = {}
        response['monsterloc'] = chosen_monster
        response['userloc'] = {}
        response['userloc']['latitude'] = user_latitude
        response['userloc']['longitude'] = user_longitude
        response['num'] = len(chosen_monster)
        response['new_monster_num'] = new_monster_num
        response['lower'] = lat_lower_bound
        response['upper'] = lat_upper_bound
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
