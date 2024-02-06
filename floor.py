import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px


geojson_data = gpd.read_file('C:/Users/한대희/Desktop/project1/sampled_data2.geojson')


geojson_data['circle_size'] = geojson_data['층'].apply(lambda x: max(0, x) * 10)


st.title('자치구별 층수 시각화')

fig = px.scatter_mapbox(
    geojson_data,
    lat=geojson_data.geometry.centroid.y,
    lon=geojson_data.geometry.centroid.x,
    color='층',
    size='circle_size',
    hover_name='자치구명',
    mapbox_style="carto-positron",
    center={"lat": geojson_data.geometry.centroid.y.mean(), "lon": geojson_data.geometry.centroid.x.mean()},
    zoom=10
)

st.plotly_chart(fig)