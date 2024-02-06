import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import folium


file_path = "C:/Users/한대희/Desktop/project1/sampled_data2.geojson"
gdf = gpd.read_file(file_path)


st.title('서울시 건물 평균 층수 대시보드')
st.write('이 대시보드는 서울시의 건물 데이터를 사용하여 만들어졌습니다.')

average_floors = gdf['층'].mean()
st.write(f'서울시 건물의 평균 층수: {average_floors:.2f} 층')


st.sidebar.title('메뉴')
selected_option = st.sidebar.radio('이동할 페이지를 선택하세요.', ['홈', '시각화 지도'])

if selected_option == '시각화 지도':
    # 시각화 지도 페이지
    # 자치구별 층수 시각화
    st.subheader('자치구별 층수 시각화')
    fig = px.scatter_mapbox(
        gdf,
        lat=gdf.geometry.centroid.y,
        lon=gdf.geometry.centroid.x,
        color='층',
        size=gdf['층'].apply(lambda x: max(0, x)),  
        hover_name='자치구명',
        mapbox_style="carto-positron",
        center={"lat": gdf.geometry.centroid.y.mean(), "lon": gdf.geometry.centroid.x.mean()},
        zoom=10
    )
    st.plotly_chart(fig)

elif selected_option == '홈':
    st.write('지도는 시각화 자료 페이지에 있습니다.')
