import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px
# Load CVS file from Dataset folder

def showGenre(country):

    df = pd.read_csv('netflix_titles.csv')

    NonUSDF = df[df['country'] != country].index

    df.drop(NonUSDF, inplace=True)

    df['listed_in'] = df['listed_in'].str.split(', ')
    df = df.explode('listed_in').reset_index(drop=True)
    cols = list(df.columns)
    cols.append(cols.pop(cols.index('title')))
    df = df[cols]
    newdf = pd.value_counts(df['listed_in'], sort=True)[0:10]

    newdf = pd.DataFrame({'genre':newdf.index, 'count':newdf.values})

    newdf = newdf.sample(frac=1)



    fig = px.pie(newdf, values='count', names='genre', title='Most popular genre in ' + country)

    pyo.plot(fig,filename='USGenreLineChart.html')



showGenre('France')