# Importing Dash construction methods:
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Importing main Dash projects and project layouts:
from app import app
from apps import ontario, homepage

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    # HTML Header:
    html.Div(id="html-header", className="main-header", children=[

        html.A("Velkozz Canada Job Listings Dashboard", href="/"),
    ]),

    # Main Body:
    html.Div(id='main-page-content')
])

@app.callback(
    dash.dependencies.Output("main-page-content", "children"),
    dash.dependencies.Input("url", "pathname"))
def display_page(pathname):
    """Rendering different choropleth maps for each province's
    job listings dataset. Providing routes for full application.
    """
    if pathname == "/":
        return homepage.layout

    if pathname == "/ontario":
        return ontario.layout

    else:
        return "404"

if __name__ == '__main__':
    app.run_server(debug=True)