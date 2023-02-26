import streamlit as st
import pandas as pd
import folium 
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import branca.colormap as cmp
import datetime as dt


APP_TITLE  = 'Farmland Crop Yield and Price per Bushel in the United States'
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
    ax2.set_ylabel('Dollars per bushel')
    
    st.pyplot(fig)



def display_map(df_yield, df_price):
       
    map = folium.Map(location = [38, -96.5], zoom_start = 4, scrollWheelZoom = False, tiles = 'CartoDB positron')

    states_geojson = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    df_indexed = df_yield.set_index('state')
    
    type = str(st.sidebar.selectbox('Select a crop to display on US heatmap', options=df_indexed.columns[1:]))
    color = {'barley':'Reds', 'corn':'YlOrBr', 'oats':'BuGn', 'soybeans':'YlGn'}


    choropleth = folium.Choropleth(
        geo_data = f'{states_geojson}/us-states.json',
        name = "{} Layer".format(type), 
        #geo_data = 'us-state-boundaries.geojson',
        data = df_yield,
        columns = ['state', type],
        key_on = 'feature.properties.name',
        fill_color = color[type],
        nan_fill_color = 'white',
        nan_fill_opacity = .6,
        legend_name = "Bushels per Acre of {}".format(type),
        position = 'bottomright',
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

    st_map = st_folium(map, width = 700, height = 450)

    if(st_map['last_active_drawing']):
        last_clicked = str(st_map['last_active_drawing']['properties']['name'])
        price_index = list(df_price['state']).index(last_clicked) if last_clicked in list(df_price['state']) else 'N/A'
        end_price_index = price_index
        if price_index != 'N/A':
            while df_price['state'][end_price_index] == last_clicked:
                end_price_index += 1
            print(price_index, end_price_index)
            price_vals = list(df_price.iloc[price_index:end_price_index])
            print(price_vals)
        #print(list(df_price.index))
        yield_index = list(df_yield['state']).index(last_clicked)
        yield_vals = list(df_yield.iloc[yield_index])
        temp_yield_dict = {'state':yield_vals[0], 'type':['Barley', 'Corn', 'Oats', 'Soybeans'], 'val':[yield_vals[2], yield_vals[3], yield_vals[4], yield_vals[5]]}
        temp_yield_df = pd.DataFrame(temp_yield_dict)
        
        x_axis_bar = temp_yield_df.columns[1]
        y_axis_bar = temp_yield_df.columns[2]
    
        # Plot the bar chart using the selected columns
        plot_charts(temp_yield_df, x_axis_bar, y_axis_bar)
        


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)
    
    #Load data
    df_yield = pd.read_csv('data/AllYield.csv')
    df_price = pd.read_csv('data/pr/BARLEY.csv')

    #Display filters and map
    display_map(df_yield, df_price)
    

if __name__ == "__main__":
    main()