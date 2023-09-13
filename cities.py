import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('india_cities.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Columns for waste components
waste_component_cols = [
    'Waste Components: Food (%)',
    'Waste Components: Green (%)',
    'Waste Components: Wood (%)',
    'Waste Components: Paper and Cardboard (%)',
    'Waste Components: Textiles (%)',
    'Waste Components: Plastic (%)',
    'Waste Components: Metal (%)',
    'Waste Components: Glass (%)',
    'Waste Components: Rubber/Leather (%)',
    'Waste Components: Other (%)'
]

# Create the map with appropriate basemap and zoom level
fig_map = px.scatter_geo(df,
                         lat='Latitude',
                         lon='Longitude',
                         hover_name='City',
                         hover_data=['Input Data Source'],
                         size='Emissions per Capita (kg CH4/person/year)',
                         color='Emissions per Capita (kg CH4/person/year)',
                         projection='mercator',
                         title='Emissions per Capita by City in India',
                         scope='asia',
                         center={'lat': 20.5937, 'lon': 78.9629},
                         height=600)

# Create the layout of the app
app.layout = html.Div([
    html.H1("India Cities: Emissions and Waste Components"),
    
    # Map
    dcc.Graph(id='map', figure=fig_map),
    
    # Pie Chart
    dcc.Graph(id='pie-chart')
])

# Callback to update pie chart based on selected city in map
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('map', 'clickData')]
)
def update_pie_chart(clickData):
    if clickData is None:
        return {}
    
    # Get clicked city
    clicked_city = clickData['points'][0]['hovertext']
    
    # Filter data for clicked city
    city_data = df[df['City'] == clicked_city]
    
    # Aggregate waste components
    waste_data = city_data[waste_component_cols].mean()
    
    # Create pie chart
    fig_pie = px.pie(waste_data.reset_index(), values=waste_data, names='index', title=f'Waste Components in {clicked_city}')
    return fig_pie

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
