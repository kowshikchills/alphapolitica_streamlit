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
import glob
from PIL import Image
from numerize import numerize


class IssuesPage:
    def __init__(self):
        self.df_tags_highlevel = pd.read_csv('plots_data/tags_high_level.csv')

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
        <span class="word1">AP Topics </span>
        <span class="word2">Graphs</span>
        </p>
        """, unsafe_allow_html=True)

        col1,col2 = st.columns([0.75,0.25])
        col21, col22 = col2.columns(2)
        start_date = col21.date_input(
            "Start Date",
            datetime.date(2022, 1, 1))
        end_date = col22.date_input(
            "End Date",
            datetime.date(2024, 1, 1))

        View = col2.selectbox(label='Select View',options=['view_count_average', 'view_count','negative_video_uploads', 'duration', 'comment_count'],index=1)
        media_house = col2.selectbox(label='Select Channel',options=['ALL','TV9','TV5','ABN','Sakshi'],index=0)
        topics_start, topics_end = col2.slider('Candidates',0, 250, (0, 10))

        df_bar = self.df_tags_highlevel.sort_values(View, ascending=False)
        if media_house != 'ALL':
            df_bar = df_bar[df_bar.uploader == media_house ]

        fig = px.bar(df_bar[topics_start:topics_end], y=View, x='tags',color = 'uploader', text_auto='.2s',color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'red' , 'TV9':'blue'})
        fig.update_traces(opacity=.7)
        col1.plotly_chart(fig, use_container_width=True)



    def get_personal_chart(self):

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
        <span class="word1">Topic </span>
        <span class="word2">Analysis</span>
        </p>
        """, unsafe_allow_html=True)
        st.write('##')
        tags = [i.split('plots_data/tags_data/')[1].split('.csv')[0] for i in glob.glob('plots_data/tags_data/*')]

        coll,col1,colr = st.columns(3)
        tag = col1.selectbox(label='Select topic',options=tags,index=0)
        st.write('##')  
        st.write('##') 

        file_loc = 'plots_data/tags_data/'+tag +'.csv'
        df_tag = pd.read_csv(file_loc) 
        df_tag['negativity'] = (df_tag['sentiment'] > 0)*1

        df_polar = df_tag.groupby(['tags','uploader']).agg({'duration':np.sum, 'view_count':np.sum, 'negativity':np.sum,'comment_count':np.sum, }).reset_index()

        col1,col2,col3,col4 = st.columns(4)
        col1.metric(label = 'Total Duration (hrs)', value = int(sum(df_polar['duration'].values/(60*60))))
        col2.metric(label = 'Total Views', value =numerize.numerize(int(sum(df_polar['view_count'].values))) )
        col3.metric(label = 'Total Negativity', value = np.round(np.sum(df_polar['negativity'].values)/len(df_tag),2) )
        col4.metric(label = 'Total Comments', value = numerize.numerize(int(sum(df_polar['comment_count'].values))))



        col1,col2 = st.columns(2)
        col3,col4 = st.columns(2)

        fig = px.bar_polar(df_polar, r="duration", theta="uploader",
                        color="uploader",
                        color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'red' , 'TV9':'blue'},
                        log_r=False, title='Duration', template="plotly_dark")
        fig.update_traces(opacity=.7,marker_line_color="white",marker_line_width=2)
        col1.plotly_chart(fig, use_container_width=True)

        fig = px.bar_polar(df_polar, r="view_count", theta="uploader",
                        color="uploader",color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'red' , 'TV9':'blue'},log_r=False, title='Total Views', template="plotly_dark")
                        
        fig.update_traces(opacity=.7,marker_line_color="white",marker_line_width=2)
        col2.plotly_chart(fig, use_container_width=True)

        fig = px.bar_polar(df_polar, r="negativity", theta="uploader",
                        color="uploader",color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'red' , 'TV9':'blue'},log_r=False, title='Negativity', template="plotly_dark")
        fig.update_traces(opacity=.7,marker_line_color="white",marker_line_width=2)
        col3.plotly_chart(fig, use_container_width=True)

        fig = px.bar_polar(df_polar, r="comment_count", theta="uploader",
                        color="uploader",color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'red' , 'TV9':'blue'},log_r=False, title='Comment Count', template="plotly_dark",)
        fig.update_traces(opacity=.7,marker_line_color="white",marker_line_width=2)
        col4.plotly_chart(fig, use_container_width=True)



        col2,col1 = st.columns([0.25,0.75])
        col2.write('##')  
        col2.write('##') 
        col2.write('##')
        col21, col22 = col2.columns(2)
        start_date = col21.date_input(
            "Start Date",
            datetime.date(2022, 6, 1),key='start date41')
        end_date = col22.date_input(
            "End Date",
            datetime.date(2024, 1, 1),key='start date42')

        date_start = str(start_date)
        date_end = str(end_date)

        View = col2.selectbox(label='Select View',options=['view_count_average','view_count','negativity','duration','comment_count'],index=1,key='start date43')
        media_house = col2.selectbox(label='Select Channel',options=['ALL','TV9','TV5','ABN','Sakshi'],index=0, key='start date44')

        df_tag = df_tag[(df_tag.upload_date >= date_start) & (df_tag.upload_date <= date_end)]


        df_tag = df_tag.sort_values('upload_date', ascending=True)
        df_tag['upload_date'] = pd.to_datetime(df_tag['upload_date']) 
        df_tag['view_count_average'] = df_tag['view_count']
        df_date_grouped = df_tag.groupby([pd.Grouper(key='upload_date', freq='3D'),
                        'uploader' ]).aggregate({'view_count':np.sum, 'duration':np.sum,'negativity':np.sum,'comment_count':np.sum,'view_count_average':np.mean}).reset_index()
        
        if media_house != 'ALL':
            df_date_grouped = df_date_grouped[df_date_grouped.uploader == media_house ]

        title_dict = {'view_count_average':'Total Average Views vs Date', 'view_count':'Total Views vs Date', 'negativity': 'Total Negative Uploads vs Date','duration':'Total Content Uploaded vs Date','comment_count': 'Total Comments vs Date'}
        fig = px.bar(df_date_grouped, title = title_dict[View],y=View, x='upload_date',log_y=True,color = 'uploader', text_auto='.2s',color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'red' , 'TV9':'blue'})
        fig.update_traces(opacity=.7)
        col1.plotly_chart(fig, use_container_width=True)

        df_tag = pd.read_csv(file_loc) 
        df_tag['negativity'] = (df_tag['sentiment'] > 0)*1
        faces = list(df_tag.columns[8:-1])
        df_faces_candidate = df_tag[['tags','uploader']+faces].groupby(['tags','uploader']).sum().reset_index()
        df_faces_candidate_T = df_faces_candidate.T
        df_faces_candidate_T = df_faces_candidate_T[1:]
        df_faces_candidate_T.columns = df_faces_candidate_T.iloc[0]
        df_faces_candidate_T = df_faces_candidate_T[1:]
        df_faces_candidate_T['Total'] = df_faces_candidate_T.values.sum(axis=1)
        df_faces_candidate_T = df_faces_candidate_T.sort_values('Total',ascending= False)
        df_faces_candidate_T = df_faces_candidate_T[df_faces_candidate_T.Total > np.percentile(df_faces_candidate_T.Total, 75) ]
        del df_faces_candidate_T['Total']

        df_faces_list = []
        for cols in ['ABN','Sakshi','TV5','TV9']:
            df = df_faces_candidate_T[[cols]]
            df.columns = ['count']
            df['uploader'] = cols
            df_faces_list.append(df)
        df_faces = pd.concat(df_faces_list)
        df_faces = df_faces.reset_index()
        df_faces.columns = ['person','count','uploader']

        df_attr = pd.read_excel('UIdata/alphapolitica_faces_attributes_coords.xlsx')
        id_dict = dict(zip(df_attr.image_id, df_attr.Name))
        df_faces['person'] = [id_dict[i] for i in df_faces['person']]
        fig = px.bar(df_faces, y='count', x='person', text_auto='.2s',
                    title="Persons Appeared", color='uploader',color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'red' , 'TV9':'blue'})
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        col1,col2 = st.columns([0.6,0.4])
        col1.plotly_chart(fig, use_container_width=True)

        faces = list(df_tag.columns[8:-1])
        df_fid_list =[]
        for f_id in faces:
            df_f = df_tag[df_tag[f_id]>0][['upload_date','duration','comment_count','view_count','sentiment','uploader']]
            df_f['person'] = id_dict[f_id] 
            df_fid_list.append(df_f)
        df_face_plot = pd.concat(df_fid_list)
        df_face_plot = df_face_plot.reset_index()
        del df_face_plot['index']

        df_bar_grouped = df_face_plot.groupby(['person','uploader']).agg({"sentiment": np.mean, 'view_count': np.sum, 'comment_count':np.sum,'duration':np.sum}).reset_index()
        df_bar_grouped  = df_bar_grouped.sort_values('view_count', ascending = False)
        df_bar_grouped['duration'] = df_bar_grouped['duration']/(60*60*24)
        df_bar_grouped['duration'] = np.round(df_bar_grouped['duration'],1)


        fig = px.treemap(df_bar_grouped, path=[px.Constant("Media"), 'uploader', 'person'], values='view_count',
                        color='uploader', hover_data=['duration','sentiment'],color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'ff2a26' , 'TV9':'#0000FF'})
        fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        fig.update_traces(marker=dict(cornerradius=5))
        col2.plotly_chart(fig, use_container_width=True)





