import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CVS file from Dataset folder

df1 = pd.read_csv('../Dataset/netflix_titles.csv')

app = dash.Dash()



if __name__ == '__main__':
    app.run_server()