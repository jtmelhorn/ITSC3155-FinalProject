import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
# Load CVS file from Dataset folder

def makeTVShowBarGraph():

    df = pd.read_csv('netflix_titles.csv')

    movieDF = df[df['type'] == 'Movie'].index

    df.drop(movieDF, inplace=True)

    newdf = pd.value_counts(df['country'], sort=-True)[0:10]

    newdf = pd.DataFrame({'country':newdf.index, 'count':newdf.values})


    data = [go.Bar(x=newdf['country'],y=newdf['count'])]

    layout = go.Layout(title='Amount of Netflix Available TV Shows Produced in Each Country (counting 1-10)', xaxis_title="States", yaxis_title="Number of Shows")

    fig = go.Figure(data=data,layout=layout)
    pyo.plot(fig,filename='tvshowBarchart.html')