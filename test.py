import folium
import pandas as pd

# Load the data
data = pd.read_csv('data.csv')

# Create the base map
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

# Create the first choropleth layer
layer1 = folium.Choropleth(
    geo_data='us-states.json',
    name='Layer 1',
    data=data,
    columns=['state', 'value1'],
    key_on='feature.id',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Value 1',
    highlight=True
).add_to(m)

# Create the second choropleth layer
layer2 = folium.Choropleth(
    geo_data='us-states.json',
    name='Layer 2',
    data=data,
    columns=['state', 'value2'],
    key_on='feature.id',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Value 2',
    highlight=True
).add_to(m)

# Define a function to toggle the visibility of the layers
def toggle_layers(name):
    for layer in m._children:
        if isinstance(layer, folium.map.Layer) and layer.name != name:
            layer.add_to(m)
        elif isinstance(layer, folium.map.Layer) and layer.name == name:
            layer.remove_from(m)

# Add the layer control to the map
folium.LayerControl(on_click=toggle_layers).add_to(m)

# Display the map
m