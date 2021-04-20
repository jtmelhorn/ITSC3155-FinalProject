import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
# Load CVS file from Dataset folder
from pandas import Series


def showGenreIndia():

    df = pd.read_csv('netflix_titles.csv')

    NonUSDF = df[df['country'] != 'India'].index

    df.drop(NonUSDF, inplace=True)

    df['listed_in'] = df['listed_in'].str.split(', ')
    df = df.explode('listed_in').reset_index(drop=True)
    cols = list(df.columns)
    cols.append(cols.pop(cols.index('title')))
    df = df[cols]

    newdf = pd.value_counts(df['listed_in'], sort=True)[0:10]

    newdf = pd.DataFrame({'genre': newdf.index, 'count': newdf.values})

    newdf = newdf.sample(frac=1)

    data = [go.Scatter(x=newdf['genre'], y=newdf['count'], mode='lines', name='Trend')]

    layout = go.Layout(title='Frequency of top 10 genres on Netflix in India', xaxis_title="Genres",
                       yaxis_title="Number of TV shows and Movies per genre")

    fig = go.Figure(data=data, layout=layout)
    pyo.plot(fig, filename='IndiaGenreLineChart.html')


showGenreIndia()