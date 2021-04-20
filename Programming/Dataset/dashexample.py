import pandas as pd
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependecies import Input, Output
import plotly.offline as pyo
# Load CVS file from Dataset folder

def showGenreUS():

    df = pd.read_csv('netflix_titles.csv')

    NonUSDF = df[df['country'] != 'United States'].index

    df.drop(NonUSDF, inplace=True)

    newdf = pd.value_counts(df['listed_in'], sort=True)[0:10]

    newdf = pd.DataFrame({'genre':newdf.index, 'count':newdf.values})

    newdf = newdf.sample(frac=1)

    data = [go.Scatter(x=newdf['genre'],y=newdf['count'], mode='lines',name='Trend')]

    layout = go.Layout(title='Frequency of top 10 genres on Netflix in the US', xaxis_title="Genres", yaxis_title="Number of TV shows and Movies per genre")

    fig = go.Figure(data=data,layout=layout)


    app = dash.Dash(0)

    app.layout = html.Div(children=[
        html.H1(children = "US Genre Dashboard"),
        dcc.Graph(id='')
   ])

