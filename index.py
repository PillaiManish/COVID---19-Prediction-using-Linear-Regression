import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return app1.layout
    elif pathname == '/prediction':
        return app2.layout
    elif pathname == '/visualize':
        return app3.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)