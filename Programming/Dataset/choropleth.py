import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
import country_converter as coco
# Load CVS file from Dataset folder

def makechoropleth():

    df = pd.read_csv('netflix_titles.csv')
    cc = coco.CountryConverter()
    tvshowDF = df[df['type'] == 'TV Show'].index
    print(df.columns)
    df.drop(tvshowDF, inplace=True)

    df['country'] = df['country'].str.split(', ')
    df = df.explode('country').reset_index(drop=True)
    cols = list(df.columns)
    cols.append(cols.pop(cols.index('title')))
    df = df[cols]

    newdf = pd.value_counts(df['country'], sort=True)

    newdf = pd.DataFrame({'country':newdf.index, 'count':newdf.values})

    newdf.drop_duplicates(subset=['count'], keep='last',inplace=True)


    newdf['code'] = coco.convert(names=newdf.country, to='ISO3')

    data = [dict(type='choropleth',colorscale='Rainbow', locations = newdf['code'],z=newdf['count'],text=newdf['country'])]

    layout = go.Layout(dict(title = "Movies available on Netflix Produced in Each Country-", geo = dict(showframe = True, showcoastlines=True, projection = dict(type='orthographic'))))

    fig = go.Figure(data=data,layout=layout)
    pyo.plot(fig,filename='barchart.html')

makechoropleth()