# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                            ],
                                            value='ALL',
                                            placeholder='Select a Launch Site Here',
                                            searchable=True
                                            ),
                                html.Br(),  #line break
                                html.Div(dcc.Graph(id='success-pie-chart')), #add the pie chart
                                html.Br(),  # line break

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                        2500: '2500',
                                                        5000: '5000',
                                                        7500: '7500',
                                                    10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='total success launches for each site')
        return fig
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        site_class = site_df.groupby(['class']).count()
        site_class.reset_index(inplace = True)
        fig = px.pie(site_class, values='Launch Site', 
        names = 'class', 
        title = 'Site ' + entered_site +' success launches')
        return fig
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(  Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id="payload-slider", component_property="value")]
               )
def get_scat_chart(entered_site, Payload_range):
    if entered_site == 'ALL':
        site_df = spacex_df[spacex_df["Payload Mass (kg)"]>Payload_range[0]]
        site_df = site_df[site_df["Payload Mass (kg)"]<Payload_range[1]]
        fig = px.scatter(spacex_df, x = "class", y = "Payload Mass (kg)", 
                        color="Booster Version Category")
        return fig
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        site_df = site_df[site_df["Payload Mass (kg)"]>Payload_range[0]]
        site_df = site_df[site_df["Payload Mass (kg)"]<Payload_range[1]]        
        fig = px.scatter(site_df, x="class", y="Payload Mass (kg)", 
                        color="Booster Version Category")
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
