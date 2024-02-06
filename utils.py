import streamlit as st 
import pandas as pd 

@st.cache_data
def load_data():
    data = pd.read_csv('C:\Users\한대희\Desktop\project1\sampled_data2.geojson')

    return data