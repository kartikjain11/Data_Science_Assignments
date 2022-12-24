# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# settings
header_dict = {'textAllign':'center', 'color':'#503D36','font-size':40}


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('Data/spacex_launch_dash.csv')
spacex_df['class'] = spacex_df['class'].replace([0,1], ['Fail','Success'])

max_paylod = spacex_df['Payload Mass (kg)'].max()
min_paylod = spacex_df['Payload Mass (kg)'].min()


launch_sites = spacex_df['Launch Site'].unique().tolist()
launch_sites_options = []
for site in launch_sites:
    launch_sites_dict = {}
    launch_sites_dict['label']=site
    launch_sites_dict['value']=site
    launch_sites_options.append(launch_sites_dict)

launch_sites_options.append({'label':'ALL','value':'ALL'})

def pie_chart(value='ALL'):
    if value=='ALL':
        spacex_df_val = spacex_df.copy()
    else:
        spacex_df_val = spacex_df.loc[spacex_df['Launch Site']==value]

    launch_site_pie = px.pie(spacex_df_val, names='class')

    return launch_site_pie

def scatter_chart(site='ALL', payload=[min_paylod,max_paylod]):
    if site == 'ALL':
        spacex_df_filtered = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0], payload[1])]
        fig = px.scatter(spacex_df_filtered, 'Payload Mass (kg)', 'class', color='Booster Version Category')
    else:
        print(site)
        spacex_df_filtered = spacex_df[(spacex_df['Launch Site']==site) & (spacex_df['Payload Mass (kg)'].between(payload[0], payload[1]))]
        fig = px.scatter(spacex_df_filtered, 'Payload Mass (kg)', 'class', color='Booster Version Category')
    
    return fig

# starting charts
launch_site_pie = pie_chart('ALL')
scatter_plot = scatter_chart('ALL',[min_paylod, max_paylod])

# create app
app = dash.Dash(__name__)

# app layout

app.layout = html.Div(
    children=[html.H1(
        'SpaceX Launch Records Dashboard',
        style=header_dict
    ),
    dcc.Dropdown(
        id='site-dropdown',
        options=launch_sites_options,
        value='ALL',
        placeholder='Select Site',
        searchable=True
    ),
    html.Br(),
    html.Div(
        dcc.Graph(
            id='success-pie-chart',
            figure=launch_site_pie
        )
    ),
    html.Br(),
    html.P('Payload Range (kg)'),
    dcc.RangeSlider(
        id='slider',
        min=min_paylod,
        max=max_paylod,
        step=1000
    ),
    html.Div(
        dcc.Graph(
            id='scatter',
            figure=scatter_plot
        )
    )
    
    ]
)

@app.callback(
    Output('success-pie-chart','figure'),
    Input('site-dropdown','value')
)
def pie_update(site_in):
    fig = pie_chart(site_in)
    return fig

@app.callback(
    Output('scatter','figure'),
    Input('site-dropdown','value'),
    Input('slider','value')
)
def scatter_update(site_in, payload):
    print(payload)
    if payload==None:
        payload = [min_paylod, max_paylod]
    if payload[0]==None:
        payload[0]=min_paylod
    if payload[1]==None:
        payload[1]=max_paylod
    fig = scatter_chart(site_in, payload)
    return fig

# run app
if __name__ == '__main__':
    app.run_server()