import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px
# Load CVS file from Dataset folder

def showGenre(country):

    df = pd.read_csv('netflix_titles.csv')

    NotCountry = df[df['country'] != country].index

    df.drop(NotCountry, inplace=True)

    TVshow = df[df['type'] != 'TV Show'].index

    df.drop(TVshow, inplace=True)

    newdf = pd.value_counts(df['rating'], sort=True)[0:10]

    newdf = pd.DataFrame({'rating':newdf.index, 'count':newdf.values})

    newdf = newdf.sample(frac=1)



    fig = px.pie(newdf, values='count', names='rating', title='Most popular rating in ' + country)

    pyo.plot(fig,filename='ratingByCountry.html')



showGenre('France')