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


def map_show():
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


def old_movies():
    df = pd.read_csv('netflix_titles.csv')
    del df['show_id'], df['type'], df['director'], df['date_added'], df['rating'], \
        df['duration'], df['country']
    pd.set_option('display.max_colwidth', 5)

    df.dropna(inplace=True)
    df.drop_duplicates(keep=False, inplace=True)
    # convert to string
    df = df.astype(str)
    df = df.sort_values('release_year', ascending=True)

    return df


# makes figure
def make_figure():
    mapDf = map_show()
    mapDf['Movies Produced:'] = mapDf['count']
    fig = px.choropleth(mapDf, locations="code",
                        color="Movies Produced:",
                        hover_name="country",
                        projection='orthographic',
                        color_continuous_scale=px.colors.sequential.Plasma)

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

def showGenre(country, datatype):
    df = pd.read_csv('netflix_titles.csv')

    if (country != 'All'):
        NonUSDF = df[df['country'] != country].index

        df.drop(NonUSDF, inplace=True)

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


dfCountries = list(map_show()['country'])
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
    html.A(html.Button('Movies and TV Shows available on Netflix Produced in Each Country', className='three columns',
                       style={'marginLeft': '1000px', 'margin-bottom': '10px', 'color': 'black', 'display': 'flex',
                              'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center',
                              'background-color': 'rgb(169,169,169)'}),
           href='/popular-genres'),
    html.Br(), html.Br(), html.Br(), html.Br(),
    html.A(html.Button('Most Popular Genres In Each Country', className='three columns',
                       style={'marginLeft': '1000px', 'margin-bottom': '10px', 'color': 'black', 'display': 'flex',
                              'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center',
                              'background-color': 'rgb(169,169,169)'}),
           href='/popular-ratings')
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
            value='genre',
            options=[{'value': x, 'label': x}
                     for x in showUniqueGenre()['listed_in']],
            clearable=False
        ),
        # Ratings
        html.H3('Ratings'),
        dcc.Dropdown(
            id='input_state_2',
            value='All',
            options=[{'value': x, 'label': x}
                     for x in ['All']],
            clearable=False
        ),
        html.Br(),
        html.Button(id='submit_button', n_clicks=0, children='Submit'),
        html.Div(id='output_state'),
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
    elif pathname == "/popular-genres":
        return layout_page_2
    elif pathname == "/popular-ratings":
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
    [Output(component_id='the_graph', component_property='figure')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_state', component_property='value')],
    [State(component_id='input_state_2', component_property='value')]
)
def update_output(num_clicks, val_selected, val_selected_2):
    if val_selected is None:
        raise PreventUpdate
    else:
        fig = make_figure()
        fig.update_layout()
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
