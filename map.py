import streamlit as st
import pandas as pd
import folium 
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import branca.colormap as cmp


APP_TITLE  = 'Farmland of the United States'
APP_SUBTITLE = 'Source: National Agricultural Statistics Service'

def plot_charts(df, x_axis, y_axis):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
    
    # Plot the bar chart
    ax1.bar(df[x_axis], df[y_axis])
    ax1.set_xlabel('Type of crop')
    ax1.set_ylabel('Bushels per Acre (BPA)')
    
    # Plot the line chart
    ax2.plot(df[x_axis], df[y_axis])
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Dollar per bushal')
    
    st.pyplot(fig)

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
    

    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name']
        feature['properties']['barley'] = 'Barley yield: ' + '{:,} BPA'.format(df_indexed.loc[state_name, 'barley']) if state_name in list(df_indexed.index) else 'Barley yield: N/A'
        feature['properties']['corn'] = 'Corn yield: ' + '{:,} BPA'.format(df_indexed.loc[state_name, 'corn']) if state_name in list(df_indexed.index) else 'Corn yield: N/A'
        feature['properties']['oats'] = 'Oat yield: ' + '{:,} BPA'.format(df_indexed.loc[state_name, 'oats']) if state_name in list(df_indexed.index) else 'Oat yield: N/A'
        feature['properties']['soybeans'] = 'Soybean yield: ' + '{:,} BPA'.format(df_indexed.loc[state_name, 'soybeans']) if state_name in list(df_indexed.index) else 'Soybean yield: N/A'

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'barley', 'corn', 'oats', 'soybeans'], labels = False)
    )

    folium.LayerControl().add_to(map)

    st_map = st_folium(map, width = 700, height = 450)
    if(st_map['last_active_drawing']):
        last_clicked = str(st_map['last_active_drawing']['properties']['name'])
        index = list(df['state']).index(last_clicked)
        vals = list(df.iloc[index])
        temp_dict = {'state':vals[0], 'type':['Barley', 'Corn', 'Oats', 'Soybeans'], 'val':[vals[2], vals[3], vals[4], vals[5]]}
        temp_df = pd.DataFrame(temp_dict)
        
        x_axis_bar = temp_df.columns[1]
        y_axis_bar = temp_df.columns[2]
    
        # Plot the bar chart using the selected columns
        plot_charts(temp_df, x_axis_bar, y_axis_bar)
        


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)
    
    #Load data
    df = pd.read_csv('yield/AllYield.csv')

    #Display filters and map
    display_map(df)
    

if __name__ == "__main__":
    main()