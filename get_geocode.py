# -*- coding: cp1252 -*-
# -*- coding: 850 -*-
# -*- coding: utf-8 -*-
import json

import googlemaps
import csv

gmaps = googlemaps.Client(key='')

data_locality_geo_coding = []
data_admin_area_1_geo_coding = []

country = {'code': 57, 'name': 'Colombia'}

with open('data/colombia_code.csv', newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(f'Buscando Geocoding para: {row[3]}, {row[3]}, {row[1]}, ' + country['name'])
        geocode_result = gmaps.geocode(f'{row[3]}, {row[3]}, {row[1]}, ' + country['name'])
        print(geocode_result[0])
        data_locality_geo_coding.append({
            'code_country': country['code'],
            'country': country['name'],
            'code_administrative_area_level_1': row[0],
            'administrative_area_level_1': row[1],
            'code_locality': row[2],
            'locality': row[3],
            'google': geocode_result[0]
        })

with open('data/colombia_administrative1_code.csv', newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(f'Buscando Geocoding para: {row[1]}, ' + country['name'])
        geocode_result = gmaps.geocode(f'{row[1]}, ' + country['name'])
        print(geocode_result[0])
        data_admin_area_1_geo_coding.append({
            'code_country': country['code'],
            'country': country['name'],
            'code_administrative_area_level_1': row[0],
            'administrative_area_level_1': row[1],
            'google': geocode_result[0]
        })


with open('colombia.json', 'w') as outfile:
    json.dump(data_locality_geo_coding, outfile)

with open('colombia_administrative_area_level_1.json', 'w') as outfile:
    json.dump(data_admin_area_1_geo_coding, outfile)

with open('colombia.json') as json_file:
    data = json.load(json_file)
    for p in data:
        print('locality: ' + p['locality'])

with open('colombia_administrative_area_level_1.json') as json_file:
    data = json.load(json_file)
    for p in data:
        print('administrative_area_level_1: ' + p['administrative_area_level_1'])
