import streamlit as st
import folium
import pandas as pd
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
from streamlit_folium import folium_static

def main():
    # Set up Streamlit page layout
    st.set_page_config(page_title="Folium Map with Plot Popup", layout="wide")

    # Create some example data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Create a Pandas dataframe with the data
    df = pd.DataFrame({'x': x, 'y': y})

    # Create a plot of the data
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # Convert the plot to a PNG image and encode it as base64
    png_bytes = io.BytesIO()
    fig.savefig(png_bytes, format='png')
    png_bytes.seek(0)
    png_base64 = base64.b64encode(png_bytes.read()).decode('utf-8')

    # Create a Folium map centered on the United States
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

    # Define the geojson data for the US states
    states_geojson = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'

    # Define a function to display the plot in the popup
    def plot_popup(df):
        # Create a Matplotlib figure and plot the data
        fig, ax = plt.subplots()
        ax.plot(df['x'], df['y'])
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        # Convert the plot to a PNG image and encode it as base64
        png_bytes = io.BytesIO()
        fig.savefig(png_bytes, format='png')
        png_bytes.seek(0)
        png_base64 = base64.b64encode(png_bytes.read()).decode('utf-8')

        # Create a Folium popup with the PNG image
        popup = folium.Popup(html=f'<img src="data:image/png;base64,{png_base64}" />', max_width=800)
        return popup

    # Add the geojson layer to the map and specify the popup function
    folium.GeoJson(
        f'{states_geojson}/us-states.json',
        name='geojson',
        tooltip=folium.features.GeoJsonTooltip(fields=['name'], aliases=['State:']),
        popup=plot_popup(df)
    ).add_to(m)

    # Display the Folium map in the Streamlit app
    folium_static(m)

if __name__ == "__main__":
    main()