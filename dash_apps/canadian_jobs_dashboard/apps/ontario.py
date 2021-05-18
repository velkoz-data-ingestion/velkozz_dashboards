# Importing Dash construction methods:
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Importing Plotly/Dash Packages:
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

# Importing data managment packages:
import pandas as pd
import shapefile
from io import StringIO
import geopandas as gpd
import os
import pandas as pd
import json
from datetime import date, timedelta
from pathlib import Path

# Imported Velkozz Packages:
from vdeveloper_api.velkozz_pywrapper.query_api.velkozz_api import VelkozzAPI

# Importing main Dash app object:
from app import app

# <------------------------------- Data Ingestion / Transformation ------------------------------->

# Reading Ontario Township Shapefile as a geopandas dataframe:
gdf = gpd.read_file(f"{Path(__file__).parent}/../assets/gis_data/ontario/Geographic_Township_Improved.shp").to_crs(epsg=4326)

# Connecting to the Velkozz API: TODO: Make this a configurable ENV param:
velkozz_con = VelkozzAPI(token=os.environ["VELKOZZ_API_KEY"])
max_date_val = date.today() + timedelta(days=1)

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

        dcc.Graph(id="ontario-job-map", style={}),

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



@app.callback(
    dash.dependencies.Output("ontario-job-map", "figure"),
    dash.dependencies.Input("submit-button-state", "n_clicks"),
    dash.dependencies.State("job-date-range-query", "start_date"),
    dash.dependencies.State("job-date-range-query", "end_date"),
    dash.dependencies.State("job-type-query", "value"),
    dash.dependencies.State("company-name-query", "value")  
)
def update_ontario_map(n_clicks, start_date, end_date, job, company):
    """The method queries the Velkozz API for Ontario Job listings and
    uses said data to plot the choropleth map of Ontario.

    The method is connected to the Dash app through various State callbacks.
    These callbacks specifiy input params for the velkozz query api that 
    queries formatted job listings.

    This formatted data is transformed and combined with the geopandas dataframe
    containing shapefile data for Ontario. This GIS data is then fed into the
    plotly express choropleth method to create the map figure.

    Args:
        n_clicks (int): Dummy variable tying the various input components to a single
            state.
        
        start_date (str): Start date of data to be queried from the api.
        
        end_date (str): End date of data to be queried from the api.

        job (str): The type of job to be queried from the api.

        company (str): The company posting the job listings to be queried from the api.

    Returns:
        px.choropleth: The choropleth map figure generated by the geopandas data. 
    """

    job_listings_df = velkozz_con.get_indeed_job_listings(
        start_date=start_date, end_date=end_date, job_type=job, company=company)

    def refactor_df(row):
        new_row = row.replace(", ON", "").upper()
        return new_row

    # Formatting Geopandas dataframe with job listings data:
    job_listings_df["OFFICIAL_N"] = job_listings_df["location"].apply(lambda x: refactor_df(x))
    job_listings_df["_counter"] = 1

    sorted_jobs_df = job_listings_df.groupby("OFFICIAL_N").sum()

    merged_df = gdf.merge(sorted_jobs_df, how='left', on="OFFICIAL_N").set_index('OFFICIAL_N')
    merged_df["_counter"] = merged_df["_counter"].fillna(0)

    #print(merged_df.head())

    fig = px.choropleth(
            merged_df,
            geojson = merged_df.geometry,             
            locations = merged_df.index, 
            color="_counter",
            color_continuous_scale="blues")

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0, "autoexpand":True}, 
        height=700,
        coloraxis={},
        dragmode=False,
        font_color="#dbe1e8")
    
    fig.update_layout(dict(
        coloraxis_colorbar=dict(title='Num Jobs'),
        plot_bgcolor= 'rgba(0,0,0,0)',
        paper_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)"))

    return fig

@app.callback(
    dash.dependencies.Output("job-listings-timeseries", "figure"),
    dash.dependencies.Input("submit-button-timeseries-state", "n_clicks"),
    dash.dependencies.State("town-listings-selector-dropdown", "value"),
    dash.dependencies.State("job-timeseries-range-query", "start_date"),
    dash.dependencies.State("job-timeseries-range-query", "end_date"),
    dash.dependencies.State("timeseries-job-type", "value"),
    dash.dependencies.State("timeseries-company-name-query", "value")
)
def update_town_jobs_timeseries(n_clicks, town, start_date, end_date, job, company):
    """The method queries the velkozz api for job listings of a specifc location,
    groups the jobs listed in said location by day and plots a timeseries of the 
    number of listings.

    Args:
        n_clicks (int): Dummy variable tying the various input components to a single
            state.
        
        start_date (str): Start date of data to be queried from the api.
        
        end_date (str): End date of data to be queried from the api.

        job (str): The type of job to be queried from the api.

        company (str): The company posting the job listings to be queried from the api.

    Return:
        px.line: The timeseries of the number of listings for the specific location. 
    """
    # Querying the job listings data for a specific town:
    town_job_listings = velkozz_con.get_indeed_job_listings(
        start_date=start_date, end_date=end_date,
        company=company, job_type=job,
        location=town)

    # Adding a counter param to the dataframe to refactor:
    town_job_listings["_counter"] = 1

    # Grouping by individual days to create counts of listings by day:
    daily_job_listings_df = town_job_listings.groupby("date_posted").sum()
    
    # Creating timeseries plot of job listings: 
    fig = px.bar(
        daily_job_listings_df, 
        x=daily_job_listings_df.index, 
        y=daily_job_listings_df._counter)

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        font_color="#dbe1e8",
        title=f"{town} Job Listings",
        xaxis_title="Date",
        yaxis_title="Num Jobs")
    
    return fig
