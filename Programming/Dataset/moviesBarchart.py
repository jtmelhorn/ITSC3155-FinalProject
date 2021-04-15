import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
# Load CVS file from Dataset folder

def makeMovieBarchart():
    df = pd.read_csv('netflix_titles.csv')

    tvshowDF = df[df['type'] == 'TV Show'].index

    df.drop(tvshowDF, inplace=True)

    newdf = pd.value_counts(df['country'], sort=True)[0:10]

    newdf = pd.DataFrame({'country':newdf.index, 'count':newdf.values})

    data = [go.Bar(x=newdf['country'],y=newdf['count'])]

    layout = go.Layout(title='Amount of Netflix Available Movies Produced in Each Country (counting 1-10)', xaxis_title="States", yaxis_title="Number of movies")

    fig = go.Figure(data=data,layout=layout)
    pyo.plot(fig,filename='barchart.html')