import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import folium
from streamlit_folium import folium_static

file_path = "./sampled_data2.geojson"
gdf = gpd.read_file(file_path)

st.title('서울시 건물 평균 층수 대시보드')
st.write('이 대시보드는 서울시의 건물 데이터를 사용하여 만들어졌습니다.')

average_floors = gdf['층'].mean()

st.write(f'서울시 건물의 평균 층수: {average_floors:.2f} 층')

st.sidebar.title('메뉴')
selected_option = st.sidebar.radio('이동할 페이지를 선택하세요.', ['홈', '시각화 지도'])

if selected_option == '홈':

    st.subheader('메인')

elif selected_option == '시각화 지도':
   
    sub_option = st.sidebar.radio('페이지를 선택하세요.', ['시각화 지도', '막대 그래프', '히트맵'])

    if sub_option == '시각화 지도':
        st.subheader('서울시의 건물 분포:')
        m = folium.Map(location=[37.5665, 126.978], zoom_start=12)
        for idx, row in gdf.iterrows():
            center = row.geometry.centroid
            lat, lon = center.y, center.x
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                color='blue',
                fill=True,
                fill_color='blue',
                popup=f"층수: {row['층']}"
            ).add_to(m)
        
        for idx, row in gdf.iterrows():
            center = row.geometry.centroid
            lat, lon = center.y, center.x
            folium.CircleMarker(
                location=[lat, lon],
                radius=row['층'] * 0.5,  
                color='red',
                fill=True,
                fill_color='red',
                popup=f"층수: {row['층']}"
            ).add_to(m)
        folium_static(m)  

    elif sub_option == '막대 그래프':
        st.subheader('자치구별 층수 시각화')
        fig = px.bar(
            gdf.groupby('자치구명')['층'].mean().reset_index(),  
            x='자치구명',
            y='층',
            title='자치구별 평균 층수',
            labels={'층': '평균 층수', '자치구명': '자치구'},
            height=400
        )
        st.plotly_chart(fig)

    elif sub_option == '히트맵':
       
        st.subheader('서울시 건물 층 수 분포 히트맵')
        gdf['centroid_lat'] = gdf.geometry.centroid.y
        gdf['centroid_lon'] = gdf.geometry.centroid.x
        fig = px.density_mapbox(
            gdf, 
            lat='centroid_lat', 
            lon='centroid_lon', 
            z='층', 
            radius=10,
            center=dict(lat=37.5665, lon=126.978),
            zoom=10,
            mapbox_style="carto-positron",
            title="서울시 건물 층 수 분포",
        )
        st.plotly_chart(fig)
