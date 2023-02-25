import streamlit as st
import pandas as pd
import folium 
from streamlit_folium import st_folium
import branca.colormap as cmp


APP_TITLE  = 'Farmland of the United States'
APP_SUBTITLE = 'Source: National Agricultural Statistics Service'

def display_map(df):
       
    map = folium.Map(location = [38, -96.5], zoom_start = 4, scrollWheelZoom = False, tiles = 'CartoDB positron')

    states_geojson = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    df_indexed = df.set_index('state')
    
    choropleth = folium.Choropleth(
        geo_data = f'{states_geojson}/us-states.json',
        name = "choropleth", 
        #geo_data = 'us-state-boundaries.geojson',
        data = df,
        columns = ['state', 'corn'],
        #columns = 'state, barley, corn, oats, soybeans',
        key_on = 'feature.properties.name',
        fill_color = 'YlGnBu',
        legend_name = "Bushels per Acre of Corn",
        fill_opacity = .8,
        line_opacity = 0.8,
        highlight = True,
        
        )
    
    choropleth.geojson.add_to(map)
    #folium.LayerControl().add_to(map)

    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name']
        feature['properties']['barley'] = 'Barley yield: ' + '{:,} BPA'.format(df_indexed.loc[state_name, 'barley']) if state_name in list(df_indexed.index) else 'Barley yield: N/A'
        feature['properties']['corn'] = 'Corn yield: ' + '{:,} BPA'.format(df_indexed.loc[state_name, 'corn']) if state_name in list(df_indexed.index) else 'Corn yield: N/A'
        feature['properties']['oats'] = 'Oat yield: ' + '{:,} BPA'.format(df_indexed.loc[state_name, 'oats']) if state_name in list(df_indexed.index) else 'Oat yield: N/A'
        feature['properties']['soybeans'] = 'Soybean yield: ' + '{:,} BPA'.format(df_indexed.loc[state_name, 'soybeans']) if state_name in list(df_indexed.index) else 'Soybean yield: N/A'

    choropleth.geojson.add_child(
        #folium.features.GeoJsonTooltip(['name', 'barley'], labels = False)
        folium.features.GeoJsonTooltip(['name', 'barley', 'corn', 'oats', 'soybeans'], labels = False)
    )

    st_map = st_folium(map, width = 700, height = 450)


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)
    
    #Load data
    #continental = pd.read_csv('Continental_fraud.csv')
    df = pd.read_csv('yield/AllYield.csv')

    #st.write(df_barley.shape)
    #st.write(df_barley.head())
    #st.write(df_barley.columns)
    #Display filters and map
    display_map(df)
    
    
    
    #Display metrics




if __name__ == "__main__":
    main()