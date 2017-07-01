import requests
import re
import json
import os
import time
from datetime import datetime as dt
import pickle
import pandas as pd

wiki_url = 'https://en.wikipedia.org/wiki/Lists_of_American_films'
base_wiki = 'https://en.wikipedia.org'
tmdb_url = 'https://api.themoviedb.org/3/search/movie?api_key='
tmdb_query = '&language=en-US&query=%s&page=1'

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

response = requests.get(wiki_url, headers=header_data)

query = '<li><a href="(.+?)" title=".+?">.+?</a></li>'
year_list = re.compile(query, re.DOTALL).findall(response.text)
movie_list = []

for year_link in year_list:
    try:
        current_year = int(year_link.split('_')[-1])
    except ValueError:
        # end of list is all stuff I don't care about
        break

    response = requests.get(base_wiki+year_link, headers=header_data)
    mt_query = '<td><i><a href=".+?" title=".+?">(.+?)</a></i></td>'
    temp_movie_list = re.compile(mt_query, re.DOTALL).findall(response.text)
    movie_list.extend([(x, current_year) for x in temp_movie_list])

tmdb_key = os.environ['TMDB_key']
movie_dict = {}

# everything below is duplicated from scrape_tv
# and should be turned into a function
print('I am going to loop through {} movies'.format(len(movie_list)))
for i, movie in enumerate(movie_list):
    time.sleep(0.3)
    if i % 10 == 0:
        print('I am on movie number {}, which is named {}'.format(
            i, movie[0]))

    movie_name = movie[0]
    if movie_name.find('(') > 0:
        movie_name = movie_name[:movie_name.find('(')]
    movie_name = movie_name.replace(" ", "%20")

    start = movie[1]

    url = tmdb_url+tmdb_key+tmdb_query % (movie_name)
    response = requests.get(url, headers=header_data)
    while response.status_code == 429 or response.status_code == 401:
        time.sleep(120)
        response = requests.get(tmdb_url, headers=header_data)

    json_response = json.loads(response.text)
    if json_response['total_results'] > 0:
        for a_result in json_response['results']:
            air_date = a_result['release_date']

            result_test = air_date.split('-')[0] == str(start)

            if result_test:
                movie_name = movie_name.replace("%20", " ")
                if movie_name in movie_dict:
                    unique_movie_count += 1
                    movie_name += '_{}'.format(unique_movie_count)
                    movie_dict[movie_name] = a_result
                else:
                    unique_movie_count = 0
                    movie_dict[movie_name] = a_result

with open('movie.pickle', 'wb') as handle:
    pickle.dump(movie_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
