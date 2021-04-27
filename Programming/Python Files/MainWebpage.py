import pandas as pd
import numpy as np

import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import country_converter as coco

# Load CVS file from Dataset folder

df_perm = pd.read_csv('netflix_titles.csv')

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

mapDf = pd.value_counts(df['country'], sort=True)

mapDf = pd.DataFrame({'country': mapDf.index, 'count': mapDf.values})

mapDf.drop_duplicates(subset=['count'], keep='last', inplace=True)

mapDf['code'] = coco.convert(names=mapDf.country, to='ISO3')


def old_movies():
    df = pd.read_csv('netflix_titles.csv')
    del df['show_id'], df['type'], df['director'], df['date_added'], df['rating'], \
        df['duration'], df['country']
    pd.set_option('display.max_colwidth', 5)

    df.dropna(inplace=True)
    df.drop_duplicates(keep=False, inplace=True)
    #convert to string
    df = df.astype(str)
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

    newdf = pd.DataFrame({'country': newdf.index, 'count': newdf.values})

    newdf.drop_duplicates(subset=['count'], keep='last', inplace=True)

    return newdf


def make_figure():
    # if val_selected is None:
    #     raise PreventUpdate
    # else:
    fig = px.choropleth(mapDf, locations="code",
                        color="count",
                        hover_name="country",
                        projection='orthographic',
                        title='Movies Produced',
                        color_continuous_scale=px.colors.sequential.Plasma)

    # fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
    #                   margin=dict(l=60, r=60, t=50, b=50))

    return fig


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

    newdf = pd.DataFrame({'genre': newdf.index, 'count': newdf.values})

    newdf = newdf.sample(frac=1)

    return newdf


dfCountries = list(make_choropleth()['country'])

oldMoviesTable = old_movies()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
    html.H2(children = 'Welcome To NetAvail!',style={'textAlign':'center'}),
    html.A(html.Button('Search For Old Films', className='three columns'),
           href='/old-films'),
    html.Br(), html.Br(),
    html.A(html.Button('Movies available on Netflix Produced in Each Country', className='three columns'),
           href='/popular-genres'),
    html.Br(), html.Br(),
    html.A(html.Button('Most Popular Genres In Each Country', className='three columns'),
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
    html.H2('Movies available on Netflix Produced in Each Country'),
    html.Div([
        dcc.Graph(id='the_graph', figure=make_figure())
    ])
])

layout_page_3 = html.Div([
    html.H2('Most Popular Genres In Each Country'),
    html.P("Names:"),
    dcc.Dropdown(
        id='names',
        value='United States',
        options=[{'value': x, 'label': x}
                 for x in dfCountries],
        clearable=False
    ),
    dcc.Graph(id="pie-chart")
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


@app.callback(

    Output("pie-chart", "figure"),
    [Input("names", "value")])
def generate_chart(names):
    fig = px.pie(showGenre(names), values='count', names='genre')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
