import requests
import re
import json
import os
import time
from datetime import datetime as dt
import pickle

wiki_url = 'https://en.wikipedia.org/wiki/List_of_American_television_series'
tmdb_url = 'https://api.themoviedb.org/3/search/tv?api_key='
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

query = '<li><i><a href="/wiki/.+?" title="(.+?)">.+?</a></i> \((.+?)\)'
show_list = re.compile(query, re.DOTALL).findall(response.text)
tmdb_key = os.environ['TMDB_key']
show_dict = {}

print('I am going to loop through {} shows'.format(len(show_list)))
for i, show in enumerate(show_list):
    time.sleep(0.3)
    if i % 10 == 0:
        print('I am on show number {}, which is named {}'.format(
            i, show[0]))

    show_name = show[0]
    if show_name.find('(') > 0:
        show_name = show_name[:show_name.find('(')]
    show_name = show_name.replace(" ", "%20")

    start_end = show[1].split('–')
    if isinstance(start_end, str):
        start = start_end
    else:
        try:
            datetime_object = str(dt.strptime(start_end[0], '%B %d, %Y ').year)
        except ValueError:
            start = start_end[0]

    url = tmdb_url+tmdb_key+tmdb_query % (show_name)
    response = requests.get(url, headers=header_data)
    while response.status_code == 429 or response.status_code == 401:
        time.sleep(120)
        response = requests.get(tmdb_url, headers=header_data)

    json_response = json.loads(response.text)
    if json_response['total_results'] > 0:
        for a_result in json_response['results']:
            country = a_result['origin_country']
            air_date = a_result['first_air_date']
            if len(country) == 0:
                continue

            result_test = ((country == 0) or (country[0] == 'US')
                           and air_date.split('-')[0] == start)

            if result_test:
                show_name = show_name.replace("%20", " ")
                if show_name in show_dict:
                    unique_show_count += 1
                    show_name += '_{}'.format(unique_show_count)
                    show_dict[show_name] = a_result
                else:
                    unique_show_count = 0
                    show_dict[show_name] = a_result

with open('shows.pickle', 'wb') as handle:
    pickle.dump(show_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
