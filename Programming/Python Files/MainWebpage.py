import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# very important -- pip3 install coco
import country_converter as coco

# Load CVS file from Dataset folder
df_perm = pd.read_csv('netflix_titles.csv')


def map_get():
    df = pd.read_csv('netflix_titles.csv')
    # coco allows us to get the country codes since they weren't added in the data set
    cc = coco.CountryConverter()
    df['country'] = df['country'].str.split(', ')
    df = df.explode('country').reset_index(drop=True)
    cols = list(df.columns)
    cols.append(cols.pop(cols.index('title')))
    df = df[cols]

    mapDf = pd.value_counts(df['country'], sort=True)

    mapDf = pd.DataFrame({'country': mapDf.index, 'count': mapDf.values})

    mapDf.drop_duplicates(subset=['count'], keep='last', inplace=True)

    mapDf['code'] = coco.convert(names=mapDf.country, to='ISO3')

    return mapDf


def map_show(genre = 'Any', rating = 'Any'):
    #print(genre,rating)
    df = pd.read_csv('netflix_titles.csv')
    # coco allows us to get the country codes since they weren't added in the data set
    cc = coco.CountryConverter()
    df['country'] = df['country'].str.split(', ')
    df = df.explode('country').reset_index(drop=True)
    cols = list(df.columns)
    cols.append(cols.pop(cols.index('title')))
    df = df[cols]

    if genre != 'Any':
        df['listed_in'] = df['listed_in'].str.split(', ')
        df = df.explode('listed_in').reset_index(drop=True)
        cols = list(df.columns)
        cols.append(cols.pop(cols.index('title')))
        # sorts out americanized data
        df = df[cols]
        df = df[df['listed_in'] != 'International TV Shows']
        df = df[df['listed_in'] != 'International Movies']
        df = df[df['listed_in'] != 'British TV Shows']
        #df = df.drop_duplicates(subset='listed_in', keep='first')
        genredf = df[df['listed_in'] != genre].index
        df.drop(genredf, inplace=True)
    if rating != 'Any':
        ratingdf = df[df['rating'] != rating].index
        df.drop(ratingdf, inplace=True)

    mapDf = pd.value_counts(df['country'], sort=True)

    mapDf = pd.DataFrame({'country': mapDf.index, 'count': mapDf.values})

    mapDf.drop_duplicates(subset=['count'], keep='last', inplace=True)

    mapDf['code'] = coco.convert(names=mapDf.country, to='ISO3')

    return mapDf


def old_movies():
    df = pd.read_csv('netflix_titles.csv')
    del df['show_id'], df['type'], df['director'], df['date_added'], df['rating'], \
        df['duration']
    pd.set_option('display.max_colwidth', 5)

    df.dropna(inplace=True)
    df.drop_duplicates(keep=False, inplace=True)
    # convert to string
    df = df.astype(str)
    df = df.sort_values('release_year', ascending=True)

    return df


# makes figure
def make_figure(genre = 'Any', rating = 'Any'):
    mapDf = map_show(genre, rating)
    mapDf['Movies Produced:'] = mapDf['count']
    #print(mapDf)
    fig = px.choropleth(mapDf, locations="code",
                        color="Movies Produced:",
                        hover_name="country",
                        projection='natural earth',
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(height=1000)
    return fig


def showUniqueGenre():
    df = pd.read_csv('netflix_titles.csv')

    df['listed_in'] = df['listed_in'].str.split(', ')
    df = df.explode('listed_in').reset_index(drop=True)
    cols = list(df.columns)
    cols.append(cols.pop(cols.index('title')))
    # sorts out americanized data
    df = df[cols]
    df = df[df['listed_in'] != 'International TV Shows']
    df = df[df['listed_in'] != 'International Movies']
    df = df[df['listed_in'] != 'British TV Shows']
    df = df.drop_duplicates(subset='listed_in', keep='first')

    return df

def showUniqueRating():
    df = pd.read_csv('netflix_titles.csv')

    df['listed_in'] = df['listed_in'].str.split(', ')
    df = df.explode('listed_in').reset_index(drop=True)
    cols = list(df.columns)
    cols.append(cols.pop(cols.index('title')))
    # sorts out americanized data
    df = df[cols]
    df = df[df['listed_in'] != 'International TV Shows']
    df = df[df['listed_in'] != 'International Movies']
    df = df[df['listed_in'] != 'British TV Shows']
    df = df.drop_duplicates(subset='listed_in', keep='first')
    df = df.drop_duplicates(subset='rating',keep='first')

    return df


def showGenre(country, datatype):
    df = pd.read_csv('netflix_titles.csv')

    df['country'] = df['country'].str.split(', ')
    df = df.explode('country').reset_index(drop=True)
    cols = list(df.columns)
    cols.append(cols.pop(cols.index('title')))
    df = df[cols]

    if (country != 'All'):
        NonUSDF = df[df['country'] != country].index

        df.drop(NonUSDF, inplace=True)
    if(datatype == 'genre'):
        df['listed_in'] = df['listed_in'].str.split(', ')
        df = df.explode('listed_in').reset_index(drop=True)
        cols = list(df.columns)
        cols.append(cols.pop(cols.index('title')))
        # sorts out americanized data
        df = df[cols]
    df = df[df['listed_in'] != 'International TV Shows']
    df = df[df['listed_in'] != 'International Movies']
    df = df[df['listed_in'] != 'British TV Shows']
    newdf = pd.value_counts(df['listed_in' if datatype == 'genre' else 'rating'], sort=True)[0:10]
    newdf = pd.DataFrame({datatype: newdf.index, 'count': newdf.values})

    newdf = newdf.sample(frac=1)

    return newdf


dfCountries = list(map_get()['country'])
dfCountries.insert(0, 'All')

oldMoviesTable = old_movies()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
    html.H2(children='Welcome To NetAvail!',
            style={'textAlign': 'center', 'background-color': 'rgb(0,0,0)', 'margin-top': '0px', 'color': 'red'}),
    html.Br(), html.Br(), html.Br(), html.Br(),
    html.A(html.Button('Search For TV Shows and Movies', className='three columns',
                       style={'margin-left': '1000px', 'margin-bottom': '10px', 'color': 'black', 'display': 'flex',
                              'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center',
                              'background-color': 'rgb(169,169,169)'}),
           href='/old-films'),
    html.Br(), html.Br(), html.Br(), html.Br(),
    html.A(html.Button('Search Where the Movies Were Produced', className='three columns',
                       style={'marginLeft': '1000px', 'margin-bottom': '10px', 'color': 'black', 'display': 'flex',
                              'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center',
                              'background-color': 'rgb(169,169,169)'}),
           href='/movies-produced'),
    html.Br(), html.Br(), html.Br(), html.Br(),
    html.A(html.Button('Most Popular Categories In Each Country', className='three columns',
                       style={'marginLeft': '1000px', 'margin-bottom': '10px', 'color': 'black', 'display': 'flex',
                              'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center',
                              'background-color': 'rgb(169,169,169)'}),
           href='/popular-categories')
])

layout_page_1 = html.Div([
    html.H2('Search for TV Shows and Movies',
            style={'textAlign': 'center', 'background-color': 'rgb(0,0,0)', 'margin-top': '0px', 'color': 'red'}),
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
    html.H2('TV Shows and Movies available on Netflix Produced in Each Country',
            style={'textAlign': 'center', 'background-color': 'rgb(0,0,0)', 'margin-top': '0px', 'color': 'red'}),
    html.Div([
        dcc.Graph(id='the_graph', figure=make_figure())
    ]),

    html.Div([
        # Genre
        html.H3('Genre'),
        dcc.Dropdown(
            id='input_state',
            value='Any',
            options=[{'value': x, 'label': x}
                     for x in ['Any'] + list(showUniqueGenre()['listed_in'])],
            clearable=False
        ),
        # Ratings
        html.H3('Ratings'),
        dcc.Dropdown(
            id='input_state_2',
            value='Any',
            options=[{'value': x, 'label': x}
                     for x in ['Any']+list(showUniqueRating()['rating'])],
            clearable=False
        )
    ], style={'text-align': 'center'})

])

layout_page_3 = html.Div([
    html.H2('Most Popular Genres In Each Country',
            style={'textAlign': 'center', 'background-color': 'rgb(0,0,0)', 'margin-top': '0px', 'color': 'red'}),
    html.P("Countries:"),
    dcc.Dropdown(
        id='names',
        value='All',
        options=[{'value': x, 'label': x}
                 for x in dfCountries],
        clearable=False
    ),
    dcc.Dropdown(
        id='datatype',
        value='genre',
        options=[{'value': x, 'label': x}
                 for x in ['genre', 'ratings']],
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
    elif pathname == "/movies-produced":
        return layout_page_2
    elif pathname == "/popular-categories":
        return layout_page_3
    else:
        return layout_index


@app.callback(
    Output("pie-chart", "figure"),
    [Input("names", "value")],
    [Input("datatype", "value")]
)
def generate_chart(names, datatype):
    fig = px.pie(showGenre(names, datatype), values='count', names=datatype)
    return fig


@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input("input_state", "value")],
    [Input("input_state_2", "value")]
)
def update_output(input_state, input_state_2):
    if input_state is None and input_state_2 is None:
        raise PreventUpdate
    else:
        fig = make_figure(input_state, input_state_2)
        fig.update_layout(height=1000)
        fig.update_layout()
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
