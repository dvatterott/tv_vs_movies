import requests
import json
import os
import pickle

tmdb_url = 'https://api.themoviedb.org/3/genre/movie/list?api_key='
tmdb_query = '&language=en-US'

header_data = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 '
        'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'
        ',image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }


tmdb_key = os.environ['TMDB_key']
url = tmdb_url+tmdb_key+tmdb_query
response = requests.get(url, headers=header_data)

json_response = json.loads(response.text)

out_dict = {}
for i in json_response['genres']:
    out_dict[i['id']] = i['name']

print(out_dict)

with open('movie_genres.pickle', 'wb') as handle:
    pickle.dump(out_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

tmdb_url = 'https://api.themoviedb.org/3/genre/tv/list?api_key='

url = tmdb_url+tmdb_key+tmdb_query
response = requests.get(url, headers=header_data)

json_response = json.loads(response.text)

out_dict = {}
for i in json_response['genres']:
    out_dict[i['id']] = i['name']

print(out_dict)

with open('show_genres.pickle', 'wb') as handle:
    pickle.dump(out_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
