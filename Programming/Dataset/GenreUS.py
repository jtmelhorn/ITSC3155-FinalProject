import pandas as pd
import plotly.graph_objs as go
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
    pyo.plot(fig,filename='USGenreLineChart.html')