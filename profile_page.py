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
        col21, col22 = col2.columns(2)
        start_date = col21.date_input(
            "Start Date",
            datetime.date(2022, 1, 1))
        end_date = col22.date_input(
            "End Date",
            datetime.date(2024, 1, 1))

        View = col2.selectbox(label='Select View',options=['view_count_average','view_count','negative_video_uploads'],index=1)
        media_house = col2.selectbox(label='Select Channel',options=['ALL','TV9','TV5','ABN','Sakshi'],index=0)
        candidates_start, candidates_end = col2.slider('Candidates',0, 250, (0, 10))
        df_bar = self.df_persons.sort_values(View, ascending=False)
        if media_house != 'ALL':
            df_bar = df_bar[df_bar.uploader == media_house ]

        fig = px.bar(df_bar[candidates_start:candidates_end], y=View, x='name',color = 'uploader', text_auto='.2s',color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'red' , 'TV9':'blue'})
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
        <span class="word1">Candidate </span>
        <span class="word2">Analysis</span>
        </p>
        """, unsafe_allow_html=True)
        st.write('##')
        candidates = [i.split('plots_data/candidates_data/')[1].split('.csv')[0] for i in glob.glob('plots_data/candidates_data/*')]

        coll,col1,colr = st.columns(3)
        candidate = col1.selectbox(label='Select Candidates',options=candidates,index=1)
        st.write('##')  
        st.write('##') 
        file_loc = 'plots_data/candidates_data/'+candidate +'.csv'
        
        df_attr = pd.read_excel('UIdata/alphapolitica_faces_attributes_coords.xlsx')
        id_dict = dict(zip(df_attr.Name, df_attr.image_id))
        fid_loc = 'alphapolitica_faces/' + id_dict[candidate]
        party_dict =  dict(zip(df_attr.Name, df_attr.party))
        cons_dict =  dict(zip(df_attr.Name, df_attr.constituency))
        
        col1,col2,_,col3,col4 = st.columns(5)
        _,colm,_ = col2.columns(3)
        logo = Image.open(fid_loc).resize((80, 80))
        col1.image(logo,  caption=candidate)
        party_name = party_dict[candidate]
        if party_name in ['YSRCP','TDP','JSP', 'BJP']:
            party_loc = 'plots_data/'+party_name+'.png'
            party_logo = Image.open(party_loc).resize((100, 100))
            colm.image(party_logo,  caption=party_name)
            try:   
                col2.info('Constituency: ' + cons_dict[candidate]) 
            except:
                a =1
        df_face = pd.read_csv(file_loc)    
        df_face = df_face[df_face.upload_date > '2022-06-01']
        df_face['negativity'] = (df_face['sentiment'] > 0)*1
        df_polar = df_face.groupby('uploader').agg({'duration':np.sum, 'view_count':np.sum, 'negativity':np.sum,'comment_count':np.sum, }).reset_index()
        col3.metric(label = 'Total Duration (hrs)', value = int(sum(df_polar['duration'].values/(60*60))))
        col3.metric(label = 'Total Views', value =numerize.numerize(int(sum(df_polar['view_count'].values))) )
        col4.metric(label = 'Total Negativity', value = np.round(np.sum(df_polar['negativity'].values)/len(df_face),2) )
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
            datetime.date(2022, 1, 1),key='start date41')
        end_date = col22.date_input(
            "End Date",
            datetime.date(2024, 1, 1),key='start date42')

        date_start = str(start_date)
        date_end = str(end_date)

        View = col2.selectbox(label='Select View',options=['view_count_average','view_count','negativity','duration','comment_count'],index=1,key='start date43')
        media_house = col2.selectbox(label='Select Channel',options=['ALL','TV9','TV5','ABN','Sakshi'],index=0, key='start date44')

        df_face = df_face[(df_face.upload_date >= date_start) & (df_face.upload_date <= date_end)]
        df_face = df_face.sort_values('upload_date', ascending=True)
        df_face['upload_date'] = pd.to_datetime(df_face['upload_date']) 
        df_face['view_count_average'] = df_face['view_count']
        df_date_grouped = df_face.groupby([pd.Grouper(key='upload_date', freq='3D'),
                        'uploader' ]).aggregate({'view_count':np.sum, 'duration':np.sum,'negativity':np.sum,'comment_count':np.sum,'view_count_average':np.mean}).reset_index()
        
        if media_house != 'ALL':
            df_date_grouped = df_date_grouped[df_date_grouped.uploader == media_house ]
        title_dict = {'view_count_average':'Total Average Views vs Date', 'view_count':'Total Views vs Date', 'negativity': 'Total Negative Uploads vs Date','duration':'Total Content Uploaded vs Date','comment_count': 'Total Comments vs Date'}
        fig = px.bar(df_date_grouped, title = title_dict[View],y=View, x='upload_date',log_y=True,color = 'uploader', text_auto='.2s',color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'red' , 'TV9':'blue'})
        fig.update_traces(opacity=.7)
        col1.plotly_chart(fig, use_container_width=True)


        tags = list(df_face.columns[11:-1])
        df_tags_candidate = df_face[['name','uploader']+tags].groupby(['name','uploader']).sum().reset_index()
        df_tags_candidate_T = df_tags_candidate.T
        df_tags_candidate_T = df_tags_candidate_T[1:]
        df_tags_candidate_T.columns = df_tags_candidate_T.iloc[0]
        df_tags_candidate_T = df_tags_candidate_T[1:]

        df_tags_candidate_T['Total'] = df_tags_candidate_T.values.sum(axis=1)
        df_tags_candidate_T = df_tags_candidate_T.sort_values('Total',ascending= False)
        del df_tags_candidate_T['Total']

        df_topics_list = []
        for cols in ['ABN','Sakshi','TV5','TV9']:
            df = df_tags_candidate_T[[cols]]
            df.columns = ['count']
            df['uploader'] = cols
            df_topics_list.append(df)
        df_topics = pd.concat(df_topics_list)
        df_topics = df_topics.reset_index()
        df_topics.columns = ['topic','count','uploader']



        fig = px.bar(df_topics, y='count', x='topic', text_auto='.2s',
                    title="Topics Covered", color='uploader',color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'red' , 'TV9':'blue'})
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        col1,col2 = st.columns([0.6,0.4])
        col1.plotly_chart(fig, use_container_width=True)


        tags = list(df_face.columns[11:-1])

        df_tid_list =[]
        for t_id in tags:
            df_tag = df_face[df_face[t_id]>0][['upload_date','duration','comment_count','view_count','sentiment','uploader']]
            df_tag['tags'] = t_id
            df_tid_list.append(df_tag)
        df_tags_plot = pd.concat(df_tid_list)
        df_tags_plot = df_tags_plot.reset_index()
        del df_tags_plot['index']

        df_bar_grouped = df_tags_plot.groupby(['tags','uploader']).agg({"sentiment": np.mean, 'view_count': np.sum, 'comment_count':np.sum,'duration':np.sum}).reset_index()
        df_bar_grouped  = df_bar_grouped.sort_values('view_count', ascending = False)
        df_bar_grouped['duration'] = df_bar_grouped['duration']/(60*60*24)
        df_bar_grouped['duration'] = np.round(df_bar_grouped['duration'],1)

        fig = px.treemap(df_bar_grouped, path=[px.Constant("Media"), 'uploader', 'tags'], values='view_count',
                        color='uploader', hover_data=['duration','sentiment'],color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'ff2a26' , 'TV9':'#0000FF'})
        fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        fig.update_traces(marker=dict(cornerradius=5))
        col2.plotly_chart(fig, use_container_width=True)



