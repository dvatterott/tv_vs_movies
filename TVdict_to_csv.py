import pandas as pd
import pickle

with open('shows.pickle', 'rb') as handle:
    show_dict = pickle.load(handle)


def clean_show_dict(show_dict):
    # i was too lazy when i made this original dictionary
    show_list = list(show_dict.keys())

    new_dict = dict((x, []) for x in show_dict[show_list[0]])

    for show in show_list:
        for key in new_dict.keys():
            new_dict[key].append(show_dict[show][key])

    new_dict['show_name'] = show_list
    return new_dict


show_dict = clean_show_dict(show_dict)
df = pd.DataFrame(show_dict)
df.to_csv('shows.csv')
