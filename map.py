import streamlit as st
import pandas as pd
import folium 
from streamlit_folium import st_folium

APP_TITLE  = 'Farmland of the United States'
APP_SUBTITLE = 'Source: National Agricultural Statistics Service'

def display_map():
       
    map = folium.Map(location = [38, -96.5], zoom_start = 4, scrollWheelZoom = False, tiles = 'CartoDB positron')
    #st.write(df.shape)
    #st.write(df.head())
    #st.write(df.columns)
    
    choropleth = folium.Choropleth(
        geo_data = 'us-state-boundaries.geojson', 
        #geo_data = 'georef-united-states-of-america-county.geojson', 
        key_on = 'feature.properties.name',
        line_opacity = 0.8,
        highlight = True
        )

    choropleth.geojson.add_to(map)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], labels = False)
    )

    st_map = st_folium(map, width = 700, height = 450)


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)
    
    #Load data
    #continental = pd.read_csv('Continental_fraud.csv')


    #Display filters and map
    display_map()
    
    
    
    #Display metrics




if __name__ == "__main__":
    main()