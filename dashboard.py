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


class Dashboard:
    def __init__(self):
        self.df_upload_plot = pd.read_csv('UIdata/uploader.csv')


    def create_data_uploader_charts(self, date_start= '2022-01-01', date_end= '2024-01-01'):

        df_bar = self.df_upload_plot
        df_bar_sorted = df_bar[(df_bar.upload_date >= date_start) & (df_bar.upload_date <= date_end)]
        df_bar_grouped = df_bar_sorted.groupby(['uploader']).agg({"sentiment": np.mean, 'view_count': np.sum, 'comment_count':np.sum,'duration':np.sum,}).reset_index()
        df_bar_grouped['uploads'] = df_bar_sorted.groupby(['uploader']).count().reset_index()['sentiment']
        df_bar_grouped  = df_bar_grouped.sort_values('view_count', ascending = False)
        df_bar_grouped['duration'] = df_bar_grouped['duration']/(60*60*25)
        df_upload_line = self.df_upload_plot.groupby(['uploader','upload_date']).aggregate({'duration':np.sum,
                                                                    'comment_count':np.sum,
                                                                    'view_count':np.sum,
                                                                    'sentiment':np.mean}).reset_index()
        df_bar_sorted = df_upload_line[(df_upload_line.upload_date >= date_start) & (df_upload_line.upload_date <= date_end)]
        df_all_upload_ = []
        for upl in ['ABN','TV5','TV9','Sakshi']:
            df_channel = df_upload_line[df_upload_line.uploader == upl].sort_values('upload_date')
            for col in ['duration','comment_count','view_count','sentiment']:
                df_channel[col] = df_channel[col].rolling(10).mean()
            df_all_upload_.append(df_channel)
        df_line_chart = pd.concat(df_all_upload_)

        self.df_piechart = df_bar_grouped
        self.df_line_chart = df_line_chart

    def show_uploader_chart(self):

        fig = px.line(self.df_line_chart, x='upload_date',
                         y='duration',
                          color='uploader',
                          color_discrete_map= {'ABN': 'yellow',
                                                'TV5': 'gold',
                                                'Sakshi':'red' , 
                                                'TV9':'blue'}, markers=False)
        st.plotly_chart(fig, use_container_width=True)

    


