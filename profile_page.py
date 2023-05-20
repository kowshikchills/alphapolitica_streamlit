import streamlit as st
import pandas as pd
import folium
import numpy as np
from folium.plugins import HeatMap
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from plotly import tools
import streamlit as st
import datetime
from streamlit_folium import st_folium


class ProfilePage:
    def __init__(self):
        self.df_persons = pd.read_csv('plots_data/profile_high_level.csv')
    def get_overall_chart(self):

        st.markdown("""
        <style>
        .word1 {
        color: #048d46;
        font-size: 35px;
        font-weight: bold;
        }

        .word2 {
        color: #0565b5;
        font-size: 35px;
        font-weight: bold;
        }
        </style>

        <p>
        <span class="word1">AP Political </span>
        <span class="word2">Personal Graphs</span>
        </p>
        """, unsafe_allow_html=True)

        col1,col2 = st.columns([0.75,0.25])
        View = col2.selectbox(label='Select View',options=['view_count_average','view_count','negative_video_uploads'],index=1)
        media_house = col2.selectbox(label='Select Channel',options=['ALL','TV9','TV5','ABN','Sakshi'],index=0)
        candidates_start, candidates_end = col2.slider('Candidates',0, 10, (0, 250))
        df_bar = self.df_persons.sort_values(View, ascending=False)
        if media_house != 'ALL':
            df_bar = df_bar[df_bar.uploader == media_house ]

        fig = px.bar(df_bar[candidates_start:candidates_end], y=View, x='name',color = 'uploader', text_auto='.2s',color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'red' , 'TV9':'blue'})
        col1.plotly_chart(fig, use_container_width=True)
