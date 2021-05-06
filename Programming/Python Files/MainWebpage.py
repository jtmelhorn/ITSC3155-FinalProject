import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import base64

# very important -- pip3 install coco
import country_converter as coco

image_filename = 'justins_creation.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


def map_get():
    """Return a list of the different countries in the dataset."""

    # make a copy of the csv file
    map_df = pd.read_csv('netflix_titles.csv')
    map_df['country'] = map_df['country'].str.split(', ')
    map_df = map_df.explode('country').reset_index(drop=True)

    cols = list(map_df.columns)
    cols.append(cols.pop(cols.index('title')))
    map_df = map_df[cols]

    map_df = pd.value_counts(map_df['country'], sort=True)

    map_df = pd.DataFrame({'country': map_df.index, 'count': map_df.values})

    map_df.drop_duplicates(subset=['count'], keep='last', inplace=True)

    # coco allows us to get the country codes since they weren't added in the data set
    map_df['code'] = coco.convert(names=map_df.country, to='ISO3')

    return map_df


def map_show(genre='Any', rating='Any'):
    """Return a panda dataframe that shows a filtered list of countries and their amount of movies
    produced based on the genre and rating of those movies.
    :param genre: A string, the genre of the movie.
    :param rating: A string, the rating of the movie."""

    map_df = pd.read_csv('netflix_titles.csv')
    map_df['country'] = map_df['country'].str.split(', ')
    map_df = map_df.explode('country').reset_index(drop=True)
    cols = list(map_df.columns)
    cols.append(cols.pop(cols.index('title')))
    map_df = map_df[cols]

    if genre != 'Any':
        map_df['listed_in'] = map_df['listed_in'].str.split(', ')
        map_df = map_df.explode('listed_in').reset_index(drop=True)
        cols = list(map_df.columns)
        cols.append(cols.pop(cols.index('title')))

        # Sorts out Americanized data
        map_df = map_df[cols]
        map_df = map_df[map_df['listed_in'] != 'International TV Shows']
        map_df = map_df[map_df['listed_in'] != 'International Movies']
        map_df = map_df[map_df['listed_in'] != 'British TV Shows']

        # Filters the genres that aren't relevant out
        genre_df = map_df[map_df['listed_in'] != genre].index
        map_df.drop(genre_df, inplace=True)

    if rating != 'Any':
        # Filters the ratings that aren't relevant out
        rating_df = map_df[map_df['rating'] != rating].index
        map_df.drop(rating_df, inplace=True)

    map_df = pd.value_counts(map_df['country'], sort=True)

    map_df = pd.DataFrame({'country': map_df.index, 'count': map_df.values})

    map_df.drop_duplicates(subset=['count'], keep='last', inplace=True)

    # coco allows us to get the country codes since they weren't added in the data set
    map_df['code'] = coco.convert(names=map_df.country, to='ISO3')

    return map_df


def films_produced():
    """Return a list of every movie on Netflix and their respective elements with the exception of what
    seems less important."""

    # Copy of csv file
    films = pd.read_csv('netflix_titles.csv')

    # Delete information the user likely wouldn't care as much about
    del films['show_id'], films['type'], films['director'], films['date_added'], films['rating'], \
        films['duration']
    pd.set_option('display.max_colwidth', 5)

    # Drop NaN values and duplicates
    films.dropna(inplace=True)
    films.drop_duplicates(keep=False, inplace=True)

    # convert to string
    films = films.astype(str)
    films = films.sort_values('release_year', ascending=True)

    return films


def make_figure(genre='Any', rating='Any'):
    """Return the choropleth representation of the filtered map data from the map_show method
    :param genre: A string, the genre of the movie.
    :param rating: A string, the rating of the movie."""

    map_df = map_show(genre, rating)
    map_df['Movies Produced:'] = map_df['count']

    fig = px.choropleth(map_df, locations="code",
                        color="Movies Produced:",
                        hover_name="country",
                        projection='natural earth',
                        color_continuous_scale='Oranges')
    fig.update_layout(height=900)

    return fig


def showUniqueGenre():
    """Return a list of unique genres available on Netflix."""

    unique = pd.read_csv('netflix_titles.csv')
    unique['listed_in'] = unique['listed_in'].str.split(', ')
    unique = unique.explode('listed_in').reset_index(drop=True)
    cols = list(unique.columns)
    cols.append(cols.pop(cols.index('title')))

    # Sorts out Americanized data
    unique = unique[cols]
    unique = unique[unique['listed_in'] != 'International TV Shows']
    unique = unique[unique['listed_in'] != 'International Movies']
    unique = unique[unique['listed_in'] != 'British TV Shows']

    unique = unique.drop_duplicates(subset='listed_in', keep='first')

    return unique


def showUniqueRating():
    """Return a list of unique ratings available on Netflix."""

    unique_df = pd.read_csv('netflix_titles.csv')
    unique_df['listed_in'] = unique_df['listed_in'].str.split(', ')
    unique_df = unique_df.explode('listed_in').reset_index(drop=True)

    cols = list(unique_df.columns)
    cols.append(cols.pop(cols.index('title')))
    unique_df = unique_df[cols]

    # Sorts out Americanized data
    unique_df = unique_df[unique_df['listed_in'] != 'International TV Shows']
    unique_df = unique_df[unique_df['listed_in'] != 'International Movies']
    unique_df = unique_df[unique_df['listed_in'] != 'British TV Shows']

    unique_df = unique_df.drop_duplicates(subset='listed_in', keep='first')
    unique_df = unique_df.drop_duplicates(subset='rating', keep='first')

    return unique_df


def showGenre(country: str, data_type: str):
    """Shifts between genre and rating for the pie chart depending on the data type; it will then return
    a dataframe of the country chosen's best categories.
    :param country: A string, the country to show in the chart.
    :param data_type: A string, rating or genre best categories."""

    # Copy data from CSV file
    df = pd.read_csv('netflix_titles.csv')
    df['country'] = df['country'].str.split(', ')
    df = df.explode('country').reset_index(drop=True)
    cols = list(df.columns)
    cols.append(cols.pop(cols.index('title')))
    df = df[cols]

    # Drop all countries but the one chosen
    if country != 'All':
        non_cndf = df[df['country'] != country].index
        df.drop(non_cndf, inplace=True)

    # More manipulation must be done to list best genre categories
    if data_type == 'genre':
        df['listed_in'] = df['listed_in'].str.split(', ')
        df = df.explode('listed_in').reset_index(drop=True)
        cols = list(df.columns)
        cols.append(cols.pop(cols.index('title')))
        df = df[cols]

    # Sorts out Americanized data
    df = df[df['listed_in'] != 'International TV Shows']
    df = df[df['listed_in'] != 'International Movies']
    df = df[df['listed_in'] != 'British TV Shows']

    # Gets the counts of the top 10 best categories based on data_type
    new_df = pd.value_counts(df['listed_in' if data_type == 'genre' else 'rating'], sort=True)[0:10]
    new_df = pd.DataFrame({data_type: new_df.index, 'count': new_df.values})

    new_df = new_df.sample(frac=1)

    return new_df


# Small necessary elements that need only run once
dfCountries = list(map_get()['country'])
dfCountries.insert(0, 'All')
films_table = films_produced()

# Dash startup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Title Page
layout_index = html.Div([
    html.H2(children='NetAvail',
            style={'textAlign': 'center', 'background-color': 'rgb(0,0,0)', 'margin-top': '0px', 'color': 'white'}),
    html.Br(),
    html.H3(
        children='Netflix has no way to see statistics about the content that is available on their platform. Someone who is interested in analyzing or creating popular content can easily fall victim to a lack of information. This may cause their creation to fail because of a Genre or Rating being unpopular in their country and culture. NetAvail allows creators to find a location that fits their niche genre as well as rating. Our app has been designed for these creators to be both intuitive and easy to understand.',
        style={'textAlign': 'center', 'border': '2px solid black', 'background-color': 'Gainsboro'}),
    html.Br(), html.Br(),
    html.Div([

        html.Div([
            html.A(html.Button('View Most Popular Movies Produced In Each Country By Genre and Rating! ',
                               className='three columns',
                               style={"margin-left": "18px", 'color': 'black',
                                      'background-color': 'rgb(169,169,169)', 'width': '100%', 'height': 'auto',
                                      'white-space': 'normal'}),
                   href='/movies-produced', id='prediction-content')], id="left", className='three columns'),

        html.Div([
            html.A(html.Button('View the Most Popular Genre and Rating In Each Country!', className='three columns',
                               style={"margin-left": "187px", 'color': 'black', 'justify-content': 'center',
                                      'background-color': 'rgb(169,169,169)', 'width': '100%', 'height': 'auto',
                                      'white-space': 'normal'}),
                   href='/popular-categories', id='prediction-content')], id="center", className='three columns'),

        html.Div([
            html.A(html.Button('Search For TV Shows and Movies', className='three columns',
                               style={"margin-left": "365px", 'color': 'black', 'justify-content': 'center',
                                      'background-color': 'rgb(169,169,169)', 'width': '100%', 'height': 'auto',
                                      'white-space': 'normal'}),
                   href='/films-produced', id='prediction-content')], id="right", className='three columns'),
    ],
        style={"display": "inline-block"}, className='row'),

    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
             style={'display': 'inline-block', 'float': 'left'}),
    html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br()
])

# Search for TV Shows and Movies Page
layout_page_1 = html.Div([
    html.H2('Search for TV Shows and Movies',
            style={'textAlign': 'center', 'background-color': 'rgb(0,0,0)', 'margin-top': '0px', 'color': 'White'}),
    html.H3(
        'Using this feature you can sort TV Shows and Movies by Title, Cast, Country, Release Year, Genre and by key words in their decription.'
        '  To do this simply type in what you are looking for in the box that says filter data under each header!',
        style={'textAlign': 'center', 'border': '2px solid black', 'background-color': 'Gainsboro'}),
    html.Br(),
    dash_table.DataTable(id='computed-table', columns=[{"name": i, "id": i} for i in films_table.columns],
                         data=films_table.to_dict('records'),
                         style_table={'overflowX': 'auto'},
                         page_size=20,
                         filter_action='native',
                         style_cell={
                             'height': 'auto',
                             # all three widths are needed
                             'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                             'whiteSpace': 'normal'},
                         style_data_conditional=[
                             {
                                 'if': {'row_index': 'odd'},
                                 'backgroundColor': 'rgb(230, 240, 250)'
                             }, {
                                 'if': {'row_index': 'even'},
                                 'backgroundColor': 'rgb(240, 245, 250)'
                             }
                         ],
                         style_header={
                             'backgroundColor': 'rgb(110, 170, 230)',
                             'fontWeight': 'bold'
                         }
                         )
])

# Search Where the Movies Were Produced Page
layout_page_2 = html.Div([
    html.H2('Most Popular Movies Produced In Each Country By Genre and Rating',
            style={'textAlign': 'center', 'background-color': 'rgb(0,0,0)', 'margin-top': '0px', 'color': 'White'}),
    html.H3(
        'This map shows you the amount of movies produced in each country sorted by either Genre or Ratings. '
        'To do this simply type in or search for the genre/rating you are looking for in the dropdown and select that option!',
        style={'textAlign': 'center', 'border': '2px solid black', 'background-color': 'Gainsboro'}),
    html.Br(),
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
                     for x in ['Any'] + list(showUniqueRating()['rating'])],
            clearable=False
        )
    ], style={'text-align': 'center'}),

    html.Div([
        dcc.Graph(id='the_graph', figure=make_figure())
    ])

])

# Most Popular Categories in Each Country
layout_page_3 = html.Div([
    html.H2('Most Popular Genre and Rating In Each Country',
            style={'textAlign': 'center', 'background-color': 'rgb(0,0,0)', 'margin-top': '0px', 'color': 'White'}),
    html.H3(
        'Using this feature you can sort and find the 10 most popular genre or rating in any available country.'
        '  To do this simply select your country from the dropdown menu!',
        style={'textAlign': 'center', 'border': '2px solid black', 'background-color': 'Gainsboro'}),
    html.Br(),
    html.P("Countries:"),
    dcc.Dropdown(
        id='names',
        value='All',
        options=[{'value': x, 'label': x}
                 for x in dfCountries],
        clearable=False
    ),
    html.Br(),
    html.Div([
        html.Div([
            html.H3('Genre'),
            dcc.Graph(id="pie-chart-genre")
        ], className="six columns"),

        html.Div([
            html.H3('Rating'),
            dcc.Graph(id="pie-chart-rating")
        ], className="six columns"),
    ], className="row")
])

# index layout
app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    layout_index,
    layout_page_2,
    layout_page_3,
    layout_page_1,
])


# Index callbacks
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    """Return the proper page to be on.
    :param pathname: A dash Input pathname, gives proper path to the page."""

    if pathname == "/films-produced":
        return layout_page_1
    elif pathname == "/movies-produced":
        return layout_page_2
    elif pathname == "/popular-categories":
        return layout_page_3
    else:
        return layout_index


# Callback for the pie chart
@app.callback(
    Output("pie-chart-genre", "figure"),
    [Input("names", "value")]
)
def genre_generate_chart(names):
    """Return a figure to the dash callback showing a pie chart of a country's most popular genre.
    :param names: A dash input value, the country name."""

    fig = px.pie(showGenre(names, 'genre'), values='count', names='genre')
    return fig


# Callback for the pie chart
@app.callback(
    Output("pie-chart-rating", "figure"),
    [Input("names", "value")]
)
def rating_generate_chart(names):
    """Return a figure to the dash callback showing a pie chart of a country's most popular rating.
    :param names: A dash input value, the country name."""

    fig = px.pie(showGenre(names, 'rating'), values='count', names='rating',
                 color_discrete_sequence=px.colors.sequential.Blackbody)
    return fig


# Callback for the map
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input("input_state", "value")],
    [Input("input_state_2", "value")]
)
def update_output(input_state, input_state_2):
    """Return a figure to the dash callback showing a map of data regarding movies produced on Netflix
    based on genre and rating.
    :param input_state: A dash input value, the genre.
    :param input_state_2: A dash input value, the rating."""

    if input_state is None and input_state_2 is None:
        raise PreventUpdate
    else:
        fig = make_figure(input_state, input_state_2)
        fig.update_layout(height=900)
        fig.update_layout()
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
