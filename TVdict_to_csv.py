import pandas as pd
import pickle

with open('shows.pickle', 'rb') as handle:
    show_dict = pickle.load(handle)

with open('show_genres.pickle', 'rb') as handle:
    genre_dict = pickle.load(handle)


def clean_show_dict(show_dict):
    # i was too lazy when i made this original dictionary
    show_list = list(show_dict.keys())

    new_dict = dict((x, []) for x in show_dict[show_list[0]])

    for show in show_list:
        for key in new_dict.keys():
            new_dict[key].append(show_dict[show][key])

    new_dict['show_name'] = show_list
    return new_dict


def fill_genre(x):
    if len(x) == 0 or x[0] not in genre_dict:
        output = 'none'
    else:
        output = genre_dict[x[0]]
    return output


show_dict = clean_show_dict(show_dict)
df = pd.DataFrame(show_dict)
df.genre_ids = df.genre_ids.apply(lambda x: fill_genre(x))
df.to_csv('shows.csv')
