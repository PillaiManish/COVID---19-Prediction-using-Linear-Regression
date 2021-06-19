import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
 
import plotly.express as px
from app import app

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
 
df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
df = df.groupby(['continent','iso_code','location'])[['total_cases']].mean()
df.reset_index(inplace=True)
print(df[:5])
 
 
# the style arguments for the sidebar.
SIDEBAR_STYLE = {
   'position': 'fixed',
   'top': 0,
   'left': 0,
   'bottom': 0,
   'width': '20%',
   'padding': '20px 10px',
   'background-color': '#333333'
}
 
# the style arguments for the main content page.
CONTENT_STYLE = {
   'margin-left': '25%',
   'margin-right': '5%',
   'top': 0,
   'padding': '20px 10px',
   
}
 
TEXT_STYLE = {
   'textAlign': 'center',
   'color': '#FFFFFF'
}
 
CARD_TEXT_STYLE = {
   'textAlign': 'center',
   'color': '#808080'
   
}
 
 
controls = dbc.FormGroup(
   [    
       
      
 
       html.P('Select Continent', style={
           'textAlign': 'center', 'color': '#FFFFFF'
       }),
       dcc.Dropdown(
           id='dropdown',
           options=[    
                {
                   'label': 'Asia',
                   'value': 'Asia'
                },
             
               {
               'label': 'North America',
               'value': 'North America'
                }, 
                {

               'label': 'South America',
               'value': 'South America'
                },
                {
                   'label': 'Africa',
                   'value': 'Africa'
                },
                

                {
                   'label': 'Oceania',
                   'value': 'Oceania'
                },
                {
                   'label': 'Europe',
                   'value': 'Europe'
                },

 
           ],
           value='Asia',  # default value
           multi=False
       ),
       html.Br(),
    #    html.P('Graph Size', style={
    #        'textAlign': 'center', 'color': '#FFFFFF'
    #    }),
    #    dcc.RangeSlider(
    #        id='range_slider',
    #        min=0,
    #        max=20,
    #        step=0.5,
    #        #value=[5, 15]
    #    ),
       
       
       html.Br(),
       dbc.Button(
           id='submit_button',
           n_clicks=0,
           children='Submit',
           color='primary',
           block=True
       ),
   ]
)
 
 
 
sidebar = html.Div(
   [    
        html.H2("COVID-19 statistics", className="display-4", style=TEXT_STYLE),
        html.Hr(),
        html.P(
            "Number of Active Deaths per Active Cases", className="lead", style={
           'textAlign': 'center', 'color': '#FFFFFF'
            }    
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/home", active="exact"),
                dbc.NavLink("Prediction", href="/prediction", active="exact"),
                dbc.NavLink("Visualization", href="https://covid-19-voila-dashboard.herokuapp.com/", active="exact", target ="_self"),
            ],
            vertical=True,
            pills=True,
            style=TEXT_STYLE
        ),
 
 
 
       html.H2('Parameters', style=TEXT_STYLE),
       html.Hr(),
       controls
   ],
   style=SIDEBAR_STYLE,
)
 
 
content = html.Div(
   [
       html.H2('Analytics Dashboard Template', style={
           'textAlign': 'center', 'color': '#000000'
        }
       ),
       html.Hr(),
       html.Div(id='output_container', children=[]),
       html.Br(),
 
       dcc.Graph(id='graphs')
       
   ],
   style=CONTENT_STYLE
)
 
 
 
layout = html.Div([sidebar, content])
 
@app.callback(
     Output('graphs','figure'),
    Input('dropdown', 'value')    #State
)
 
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
 
    container = "The Continent chosen by user was: {}".format(option_slctd)
 
    dff = df.copy()
    dff = dff[dff["continent"] == option_slctd]
 
    fig = px.choropleth(dff, locations="iso_code",
                            color="total_cases",
                            hover_name="location",
                            projection='natural earth',
                            title='Number Of Covid Cases',
                            color_continuous_scale=px.colors.sequential.Plasma)
    
    fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))
 
    
    return fig
 