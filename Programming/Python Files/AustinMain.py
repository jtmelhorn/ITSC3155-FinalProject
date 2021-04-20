import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
# Load CVS file from Dataset folder

data = pd.read_csv('netflix_titles.csv')

movieDF = pd.read_csv('netflix_titles.csv')

tvshowDF = movieDF[movieDF['type'] == 'TV Show'].index

movieDF.drop(tvshowDF, inplace=True)

newMoviedf = pd.value_counts(movieDF['country'], sort=True)[0:10]

newMoviedf = pd.DataFrame({'country':newMoviedf.index, 'count':newMoviedf.values})

movieData = [go.Bar(x=newMoviedf['country'],y=newMoviedf['count'])]

movieLayout = go.Layout(title='Amount of Netflix Available Movies Produced in Each Country (counting 1-10)', xaxis_title="States", yaxis_title="Number of confirmed cases")

#fig = go.Figure(data=movieData,layout=movieLayout)
#pyo.plot(fig,filename='barchart.html')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
    html.H2('Welcome To NetAvail!'),
    html.A(html.Button('Search For Old Films', className='three columns'),
        href='/old-films'),
    html.Br(),html.Br(),
    html.A(html.Button('Most Popular Genre In Each Country', className='three columns'),
        href='/popular-genres'),
    html.Br(),html.Br(),
    html.A(html.Button('Most Popular Ratings In Each Country', className='three columns'),
        href='/popular-ratings')
])

layout_page_1 = html.Div([
    html.H2('Old Films')
])

layout_page_2 = html.Div([
    html.H2('Most Popular Genres In Each Country')
])

layout_page_3 = html.Div([
    html.H2('Most Popular Ratings In Each Country')
])

# index layout
app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    layout_index,
    layout_page_1,
    layout_page_2,
    layout_page_3,
])


# Index callbacks
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/old-films":
        return layout_page_1
    elif pathname == "/popular-genres":
        return layout_page_2
    elif pathname == "/popular-ratings":
        return layout_page_3
    else:
        return layout_index


# # Page 1 callbacks
# @app.callback(Output('output-state', 'children'),
#               Input('submit-button', 'n_clicks'),
#               State('input-1-state', 'value'),
#               State('input-2-state', 'value'))
# def update_output(n_clicks, input1, input2):
#     return ('The Button has been pressed {} times,'
#             'Input 1 is "{}",'
#             'and Input 2 is "{}"').format(n_clicks, input1, input2)

#
# # Page 2 callbacks
# @app.callback(Output('page-2-display-value', 'children'),
#               Input('page-2-dropdown', 'value'))
# def display_value(value):
#     print('display_value')
#     return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)

