import streamlit as st
import pandas as pd
import folium 
from streamlit_folium import st_folium

APP_TITLE  = 'Farmland of the United States'
APP_SUBTITLE = 'Source: National Agricultural Statistics Service'

def display_map(df):
       
    map = folium.Map(location = [38, -96.5], zoom_start = 4, scrollWheelZoom = False, tiles = 'CartoDB positron')
    #st.write(df.shape)
    #st.write(df.head())
    #st.write(df.columns)
    states_geojson = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'

    
    
    
    choropleth = folium.Choropleth(
        geo_data = f'{states_geojson}/us-states.json',#'us-state-boundaries.geojson', 
        #geo_data = 'georef-united-states-of-america-county.geojson', 
        columns = 'state, yield_value',
        key_on = 'feature.properties.name',
        line_opacity = 0.8,
        highlight = True
        )

    choropleth.geojson.add_to(map)

    df_indexed = df.set_index('state')

    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name'].upper()
        feature['properties']['yield_value'] = 'Yield: ' + '{:,}'.format(df_indexed.loc[state_name, 'yield_value']) if state_name in list(df_indexed.index) else 'N/A'
        

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'yield_value'], labels = False)
        #folium.features.GeoJsonPopup(['name'], labels = False)
    )

    st_map = st_folium(map, width = 700, height = 450)


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)
    
    #Load data
    #continental = pd.read_csv('Continental_fraud.csv')
    df_barley = pd.read_csv('yield/BARLEY_STATES_2022.csv')

    st.write(df_barley.shape)
    st.write(df_barley.head())
    st.write(df_barley.columns)
    #Display filters and map
    display_map(df_barley)
    
    
    
    #Display metrics




if __name__ == "__main__":
    main()