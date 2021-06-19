import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from datetime import date
import plotly.graph_objs as go



# ----------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Importing the dataset
df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
df = df.dropna(axis = 0, subset = ('continent','location'))

# Get Unique Country
country = df['location'].unique()

# Get Unique Continet
continent = df['continent'].unique()


# ----------------------------------------------------------
from app import app

all_options = {}
for i in continent:
   all_options[i] = [i for i in df[df['continent']==i]['location'].unique()]
# all_options = {
#     'America': ['New York City', 'San Francisco', 'Cincinnati'],
#     'Canada': [u'Montréal', 'Toronto', 'Ottawa']
# }

layout = html.Div([
   dcc.Dropdown(
       id='countries-dropdown',
       options=[{'label': k, 'value': k} for k in all_options.keys()],
       value='Asia'
   ),

   html.Hr(),

   dcc.Dropdown(id='cities-dropdown'),

   dcc.Dropdown(
       id='types-dropdown',
       options=[{'label': 'Active Cases', 'value': 'Active Cases'}, {'label': 'Death Cases', 'value': 'Death Cases'}],
       value='Active Cases'
   ),

   dcc.Dropdown(
       id='next-dropdown',
       options=[{'label':i, 'value':i} for i in range(5,200,5)],
       value='5'
   ),


   html.Hr(),
   dcc.Graph(id='graph'),

   html.Div(id='display-selected-values')
])

@app.callback(
   dash.dependencies.Output('cities-dropdown', 'options'),
   [dash.dependencies.Input('countries-dropdown', 'value')])
def set_cities_options(selected_country):
   return [{'label': i, 'value': i} for i in all_options[selected_country]]

@app.callback(
   dash.dependencies.Output('cities-dropdown', 'value'),
   [dash.dependencies.Input('cities-dropdown', 'options')])
def set_cities_value(available_options):
   return available_options[0]['value']

@app.callback(
   dash.dependencies.Output('next-dropdown', 'value'),
   [dash.dependencies.Input('next-dropdown', 'options')])
def set_next_value(available_options):
   return available_options[0]['value']


# @app.callback(
#     dash.dependencies.Output('display-selected-values', 'children'),
#     [dash.dependencies.Input('countries-dropdown', 'value'),
#      dash.dependencies.Input('cities-dropdown', 'value')])
# def set_display_children(selected_country, selected_city):
#     return u'{} is a city in {}'.format(
#         selected_city, selected_country,
#     )

@app.callback(
   dash.dependencies.Output('graph','figure'),
   dash.dependencies.Input('cities-dropdown','value'),
   dash.dependencies.Input('types-dropdown','value'),
   dash.dependencies.Input('next-dropdown','value'),
   )
def update_graph(cities,types,next):

   if types == 'Active Cases':
       types, cond = 'new_cases', 'new_deaths'
   else:
       types, cond = 'new_deaths','new_cases'

   print(types,cond)

   df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
   df = df.fillna(0)
   df = df[df['location']==cities]

   count = df['date'].count()
   ls = [i for i in range (1,count+1)]
   df['day'] = ls


   arrnext = [i for i in range(1,next+1)]

   x, y = df[['total_cases',cond,'new_tests']],df[types]
   x_train,x_test,y_train,y_test = train_test_split(x,y)
   lr = LinearRegression().fit(x_train,y_train)
   pred = lr.predict([[df['total_cases'].iloc[-1-i], df[cond].iloc[-1-i],df['new_tests'].iloc[-1-i]] for i in range(0,next)])
   fig = go.Figure()

   fig.add_trace(go.Scatter(
                   # x=df['day'],
                   x = arrnext,
                   y=pred,
                   mode = 'lines',
                   marker = dict(
                       size = 20,
                       color = pred,
                       colorscale = 'HSV',
                       showscale = False,
                       line = dict(
                           color = 'MediumPurple',
                           width = 2
                       ))))

   # fig.add_trace(go.Scatter(
   #                 x=df['new_deaths'],
   #                 y=pred,
   #                 mode = 'lines',
   #                 marker = dict(
   #                     size = 20,
   #                     color = pred,
   #                     colorscale = 'HSV',
   #                     showscale = False,
   #                     line = dict(
   #                         color = 'MediumPurple',
   #                         width = 2
   #                     ))))
   # fig.add_trace(go.Scatter(
   #                 x=df['new_tests'],
   #                 y=pred,
   #                 mode = 'lines',
   #                 marker = dict(
   #                     size = 20,
   #                     color = pred,
   #                     colorscale = 'HSV',
   #                     showscale = False,
   #                     line = dict(
   #                         color = 'MediumPurple',
   #                         width = 2
   #                     ))))
   return fig

                    