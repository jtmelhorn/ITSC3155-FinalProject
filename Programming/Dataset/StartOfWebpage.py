import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
# Load CVS file from Dataset folder

df = pd.read_csv('netflix_titles.csv')



newdf = df[df['type'] == 'Movie']



newdf = newdf[newdf['listed_in'] == 'Dramas'].sort_values('release_year', ascending=True)[0:9]



