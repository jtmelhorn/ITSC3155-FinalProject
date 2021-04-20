import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
# Load CVS file from Dataset folder

data = pd.read_csv('netflix_titles.csv')

#movie = data[data['type']=='Movie']
#tv_show = data[data['type']=='TV Show']

#fig, ax = plot.subplots(1,1, figsize=(5, 5))
#sns.set(style='darkgrid')

#ax = sns.countplot(x = 'type', data=data, palette='Reds')

# Bar Graph of Movies Available

movieDF = pd.read_csv('netflix_titles.csv')

tvshowDF = movieDF[movieDF['type'] == 'TV Show'].index

movieDF.drop(tvshowDF, inplace=True)

newMoviedf = pd.value_counts(movieDF['country'], sort=True)[0:10]

newMoviedf = pd.DataFrame({'country':newMoviedf.index, 'count':newMoviedf.values})

movieData = [go.Bar(x=newMoviedf['country'],y=newMoviedf['count'])]

movieLayout = go.Layout(title='Amount of Netflix Available Movies Produced in Each Country (counting 1-10)', xaxis_title="States", yaxis_title="Number of confirmed cases")

#fig = go.Figure(data=movieData,layout=movieLayout)
#pyo.plot(fig,filename='barchart.html')

def display_page(pathname):
    return html.Div([
        html.H3('You are on page {}'.format(pathname))
    ])

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1('Amount of Netflix Available Movies Produced in Each Country (counting 1-10)'),
    dcc.Graph(id='graph1',
              figure={
                  'data': movieData,
                  'layout': go.Layout(title='Amount of Netflix Available Movies Produced in Each Country (counting 1-10)',
                                      xaxis={'title': 'States'}, yaxis={'title': 'Amount'})
              }
              )
])
if __name__ == '__main__':
    app.run_server(debug=True)

