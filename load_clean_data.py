import pandas as pd
import pickle

with open('shows.pickle', 'rb') as handle:
    show_dict = pickle.load(handle)

df = pd.DataFrame(show_dict)
# vote average is the percent that appears on the site.
