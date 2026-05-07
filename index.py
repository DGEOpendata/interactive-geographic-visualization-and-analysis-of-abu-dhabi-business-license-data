python
import dash
from dash import dcc, html
import dash_leaflet as dl
from dash.dependencies import Input, Output
import pandas as pd

# Load dataset (replace 'path_to_file' with the actual file path)
df = pd.read_excel('path_to_file.xlsx')

# Preprocess data
def preprocess_data(df):
    df = df.dropna(subset=['Latitude', 'Longitude'])  # Remove rows with missing coordinates
    df['City'] = df['City'].fillna('Unknown')  # Replace empty cities with 'Unknown'
    return df

data = preprocess_data(df)

# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Business License Map for Abu Dhabi, Al Ain, and Al Dhafra"),
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in data['City'].unique()],
        placeholder="Select a city",
        multi=True
    ),
    dl.Map(
        [dl.TileLayer(), dl.LayerGroup(id="layer")],
        style={'width': '100%', 'height': '500px'},
        center=[24.4539, 54.3773],
        zoom=10,
        id="map"
    )
])

@app.callback(
    Output('layer', 'children'),
    [Input('city-dropdown', 'value')]
)
def update_map(selected_cities):
    if not selected_cities:
        selected_cities = data['City'].unique()
    filtered_data = data[data['City'].isin(selected_cities)]

    markers = [
        dl.Marker(
            position=[row['Latitude'], row['Longitude']],
            children=dl.Popup([html.P(f"License: {row['LicenseNumber']}", style={'font-weight': 'bold'}),
                               html.P(f"Address: {row['Address']}")])
        )
        for _, row in filtered_data.iterrows()
    ]
    return markers

if __name__ == '__main__':
    app.run_server(debug=True)
