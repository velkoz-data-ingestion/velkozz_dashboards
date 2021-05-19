# Importing Dash construction methods:
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def build_basic_layout(gdf, max_date_val):
    """The method generates the html layout of the GIS job layout
    dashboard. 
    
    This method is used by each application page to dynamically 
    generate the html components in a base format that allows
    page specfic callbacks to be added to the base objects.

    Args:
        gdf (geopandas Dataframe): The Geopandas dataframe built
            from provincial shapefiles that is used to create the
            choropleth plot.

        max_date (datetime): A datetime value that is used to
            reprenet the maximum selectable date for the start 
            and end date query search params.

    Returns:
        html.Div: The main div tag containing all the elements
            for the choropleth map and timeseries barplot.
    
    """
    # Building the layout
    layout = html.Div([

        html.Div(id="main_graphs_div", className="main_graphs_div", children=[

            html.Div(
                id="choropleth-inputs",
                className = "choropleth_inputs",

                children=[

                    # Query Parameter Inputs:
                    dcc.DatePickerRange(
                        id="job-date-range-query",
                        display_format="YYYY/MM/DD",
                        max_date_allowed=max_date_val),

                    dcc.Input(
                        id="job-type-query",
                        type="text",
                        placeholder="Job Type"),
                    
                    dcc.Input(
                        id="company-name-query",
                        type="text",
                        placeholder="Company Name"
                    ),

                    html.Button(
                        id="submit-button-state", 
                        children="Search Jobs", 
                        style={
                            "background":"#07a15e", "color":"#dbe1e8", "border":"none"
                            }),
                ],
                style={}
            ),

            dcc.Graph(id="job-map", style={}),

            html.Div(
            id="timeseries-inputs",
            className="timeseries_inputs",

            children=[
                    dcc.Dropdown(
                        id="town-listings-selector-dropdown",
                        options = [{"label": town.title(), "value": town.title()} for town in gdf["OFFICIAL_N"].tolist()],
                        value= "Toronto"),

                    dcc.DatePickerRange(
                        id="job-timeseries-range-query",
                        display_format="YYYY/MM/DD",
                        max_date_allowed=max_date_val),
                    
                    dcc.Input(
                        id="timeseries-job-type",
                        type="text",
                        placeholder="Job Type"),

                    dcc.Input(
                        id="timeseries-company-name-query",
                        type="text",
                        placeholder="Company Name"),

                    html.Button(
                        id="submit-button-timeseries-state",
                        children="Search Jobs", 
                        style={
                            "background":"#07a15e", "color":"#dbe1e8", "border":"none"
                            }),
            ]
        ),

            dcc.Graph(id="job-listings-timeseries", style={})
        ]),
    ])

    return layout