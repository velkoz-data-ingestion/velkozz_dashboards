# Importing Dash construction methods:
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


layout = html.Div([

    # Grid System Displaying each of the Jobs Listings Dashbaord:
    html.Div(id="main-dash-grid", className="dashboard_cards_grid", children=[


        html.A(children=[html.Div(className="country_card", children=["Ontario"])], href="/ontario"),
        html.A(children=[html.Div(className="country_card", children=["British Columbia"])], href="/british_columbia"),
        html.A(children=[html.Div(className="country_card", children=["Manitoba"])], href="manitoba"),
        html.A(children=[html.Div(className="country_card", children=["Alberta"])], href="alberta"),
        html.A(children=[html.Div(className="country_card", children=["New Brunswick"])], href="new_brunswik"),
        html.A(children=[html.Div(className="country_card", children=["Newfoundland and Labrador"])], href="newfoundland_n_lab"),
        html.A(children=[html.Div(className="country_card", children=["Quebec"])], href="quebec"),
        html.A(children=[html.Div(className="country_card", children=["Saskatchewan"])], href="saskatchewan")
    ])
])