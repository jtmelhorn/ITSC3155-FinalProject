import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo


def oldMovies():
    df = pd.read_csv('netflix_titles.csv')
    del df['show_id']
    del df['type']
    del df['director']
    del df['date_added']
    del df['rating']
    del df['duration']
    del df['country']
    pd.set_option('display.max_colwidth', 5)
    #take out listed columns for "listed_in"
    df['listed_in'] = df['listed_in'].str.split(', ')
    df = df.explode('listed_in').reset_index(drop=True)
    cols = list(df.columns)
    cols.append(cols.pop(cols.index('title')))
    df = df[cols]
    #take out listed columns for "listed_in"
    df['cast'] = df['cast'].str.split(', ')
    df = df.explode('cast').reset_index(drop=True)
    cols = list(df.columns)
    cols.append(cols.pop(cols.index('title')))
    df = df[cols]

    df.dropna(inplace=True)
    df.drop_duplicates(keep = False, inplace = True)
    df = df.sort_values('release_year', ascending=True)[0:50]

    return(df)


def print_full(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')

print_full(oldMovies())