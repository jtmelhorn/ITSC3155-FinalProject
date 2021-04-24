import pandas as pd

import plotly.graph_objs as go
import plotly.offline as pyo

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

import country_converter as coco

# Load CVS file from Dataset folder


def old_movies():
    df = pd.read_csv('netflix_titles.csv')
    del df['show_id'], df['type'], df['director'], df['date_added'], df['rating'], \
        df['duration'], df['country']
    pd.set_option('display.max_colwidth', 5)

    df.dropna(inplace=True)
    df.drop_duplicates(keep=False, inplace=True)
    df = df.sort_values('release_year', ascending=True)

    return df


def make_choropleth():
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


oldMoviesTable = old_movies()

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
    html.Br(), html.Br(),
    html.A(html.Button('Most Popular Genre In Each Country', className='three columns'),
           href='/popular-genres'),
    html.Br(), html.Br(),
    html.A(html.Button('Most Popular Ratings In Each Country', className='three columns'),
           href='/popular-ratings')
])

layout_page_1 = html.Div([
    html.H2('Old Films'),
    dash_table.DataTable(id='computed-table', columns=[{"name": i, "id": i} for i in oldMoviesTable.columns],
                         data=oldMoviesTable.to_dict('records'), style_table={'overflowX': 'auto'},
                         filter_action='native',
                         style_cell={
                             'height': 'auto',
                             # all three widths are needed
                             'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                             'whiteSpace': 'normal'})
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


if __name__ == '__main__':
    app.run_server(debug=True)
