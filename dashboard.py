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
from PIL import Image

class Dashboard:
    def __init__(self):
        self.df_upload_plot = pd.read_csv('UIdata/uploader.csv')
        self.df_folium_plot = pd.read_csv('plots_data/dashboard_folium.csv')
        self.df_tags_plot = pd.read_csv('plots_data/dashboard_tags.csv')

    def show_image(self):
        col1,col2 = st.columns([0.25,0.75])

        slide = Image.open("img1.png")
        col1.write('##')
        col1.write('##')
        col1.write('##')
        col1.write('##')
        col1.image(slide)
        slide = Image.open("img2.png")
        col2.image(slide)

        _,col,_ = st.columns([0.4,0.2,0.4])
        col1.write('##')
        col1.write('##')
        col.write('Scroll down ⇩')
    
    def dashboard_create_data_uploader_charts(self, date_start= '2022-01-01', date_end= '2024-01-01'):

        df_bar = self.df_upload_plot
        df_bar_sorted = df_bar[(df_bar.upload_date >= date_start) & (df_bar.upload_date <= date_end)]
        df_bar_grouped = df_bar_sorted.groupby(['uploader']).agg({"sentiment": np.mean, 'view_count': np.sum, 'comment_count':np.sum,'duration':np.sum,}).reset_index()
        df_bar_grouped['uploads'] = df_bar_sorted.groupby(['uploader']).count().reset_index()['sentiment']
        df_bar_grouped  = df_bar_grouped.sort_values('view_count', ascending = False)
        df_bar_grouped['duration'] = df_bar_grouped['duration']/(60*60*25)
        df_bar_grouped['sentiment'] = (df_bar_grouped['sentiment'] - df_bar_grouped['sentiment'].min())/ (df_bar_grouped['sentiment'].max() - df_bar_grouped['sentiment'].min())

        df_upload_line = self.df_upload_plot.groupby(['uploader','upload_date']).aggregate({'duration':np.sum,
                                                                    'comment_count':np.sum,
                                                                    'view_count':np.sum,
                                                                    'sentiment':np.mean}).reset_index()
        df_upload_line['uploads'] = self.df_upload_plot.groupby(['uploader','upload_date']).count().reset_index()['sentiment']
        df_upload_line = df_upload_line[df_upload_line.upload_date > '2022-11-01']                                                
        df_all_upload_ = []
        for upl in ['ABN','TV5','TV9','Sakshi']:
            df_channel = df_upload_line[df_upload_line.uploader == upl].sort_values('upload_date')
            for col in ['duration','comment_count','view_count','sentiment','uploads']:
                df_channel[col] = df_channel[col].rolling(10).mean()
            df_all_upload_.append(df_channel)
        df_line_chart = pd.concat(df_all_upload_)

        self.df_piechart = df_bar_grouped
        self.df_line_chart = df_line_chart

    def dashboard_show_folium_map(self):
        col,_ =st.columns(2)
        col.markdown("""
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
        <span class="word1">Andhra Pradesh </span>
        <span class="word2">Heat Map (Total Views)</span>
        </p>
        """, unsafe_allow_html=True)

        col1,col2 = st.columns([0.72,0.25])

        col21, col22 = col2.columns(2)

        start_date = col21.date_input(
            "Start Date",
            datetime.date(2022, 1, 1))
        end_date = col22.date_input(
            "End Date",
            datetime.date(2024, 1, 1))

        date_start = str(start_date)
        date_end = str(end_date)
        media_house = col2.selectbox(label='Select Channel',options=['ALL','TV9','TV5','ABN','Sakshi'],index=0)
        candidates_start, candidates_end = col2.slider('Candidates',0, 250, (0, 250))
        to_display =col2.selectbox(label='Name vs Constituency',options=['name','constituency'],index=0) 


        df_folium_sorted = self.df_folium_plot[(self.df_folium_plot.upload_date >= date_start) &
                                                 (self.df_folium_plot.upload_date <= date_end)]
        df_folium_sorted['heat'] = df_folium_sorted['view_count']
        if media_house == 'ALL':
            del df_folium_sorted['uploader']
        else:
            df_folium_sorted = df_folium_sorted[df_folium_sorted.uploader == media_house ]
            del df_folium_sorted['uploader']
        del df_folium_sorted['upload_date']
        df_folium_sorted['view_count_mean'] = df_folium_sorted['view_count']
        df_folium_sorted = df_folium_sorted.groupby(['lat','long',
                                                     'name',
                                                     'party',
                                                     'constituency']).aggregate({'view_count': np.sum,
                                                                                'view_count_mean':np.mean,
                                                                                'sentiment':np.mean,
                                                                                'heat':np.mean}).reset_index()
        df_folium_sorted = df_folium_sorted.sort_values('view_count', ascending = False)
        df_folium_filtered = df_folium_sorted[candidates_start:candidates_end]

        df_folium_filtered_heat_map = df_folium_filtered[['lat','long','heat']]
        lats_longs_weight = df_folium_filtered_heat_map.values

        map_obj = folium.Map(location = [16.315487, 80.232213], zoom_start = 6)
        HeatMap(lats_longs_weight, min_opacit=0.2,radius=20, max_val=lats_longs_weight.T[2].max()).add_to(map_obj)

        df_markers = df_folium_filtered[['lat','long','view_count', to_display]]
        df_markers['view_count'] = (df_markers['view_count'] - df_markers['view_count'].min())/(df_markers['view_count'].max() - df_markers['view_count'].min())
        df_markers['view_count'] = (df_markers['view_count']*20)
        for i in range(len(df_markers)):
            folium.CircleMarker([df_markers['lat'].values[i], df_markers['long'].values[i]], 
                        popup=df_markers[to_display].values[i],ill=True,radius=df_markers['view_count'].values[i]
                        ).add_to(map_obj)

        with col1:
            st_data = st_folium(map_obj, width=900, height=500)

    def dashboard_show_uploader_chart(self):

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
        <span class="word1">Media </span>
        <span class="word2">Overview</span>
        </p>
        """, unsafe_allow_html=True)

        col,_,_ = st.columns(3)
        option = col.selectbox(
            'Media House Overview',
            ('Total Views',
            'Total Hours Uploaded',
            'Total Number of Comments',
            'Sentiment',
            'Number of Videos'), index = 0)
        
        button_dict = {'Total Views': 'view_count',
                        'Total Number of Comments': 'comment_count',
                        'Total Hours Uploaded': 'duration',
                        'Number of Videos': 'uploads',
                        'Sentiment': 'sentiment'}

        col1, col2 = st.columns(2)
        column_to_show = button_dict[option]
        fig1 = px.line(self.df_line_chart, x='upload_date',
                         y=column_to_show,
                          color='uploader',
                          color_discrete_map= {'ABN': 'yellow',
                                                'TV5': 'gold',
                                                'Sakshi':'red' , 
                                                'TV9':'blue'}, markers=False)
        col1.plotly_chart(fig1, use_container_width=True)
        fig2= px.pie(self.df_piechart, values=column_to_show, names='uploader',
                    title='duration Distribution',color='uploader',
                    hover_data=[column_to_show],hole=.3,color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'ff2a26' , 'TV9':'#0000FF'})
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        col2.plotly_chart(fig2, use_container_width=True)

    def dashboard_show_constituency_plots(self):

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
        <span class="word1">Andhra Constituency </span>
        <span class="word2">Graph</span>
        </p>
        """, unsafe_allow_html=True)

        col1,col2 = st.columns([0.25,0.75])
        col1.write("##")
        col1.write("##")

        col21, col22 = col1.columns(2)

        start_date = col21.date_input(
            "Start Date",
            datetime.date(2022, 1, 1), key='start date21')
        end_date = col22.date_input(
            "End Date",
            datetime.date(2024, 1, 1), key='start date22')
        date_start = str(start_date)
        date_end = str(end_date)
        candidates_start, candidates_end = col1.slider('Candidates',0, 250, (0, 10),key ='start date23')
        to_display =col1.selectbox(label='Name vs Constituency',options=['name','constituency'],index=0,key ='start date24') 


        df_bubble = self.df_folium_plot[[to_display,'upload_date','sentiment','view_count','party']]
        df_bubble_sorted = df_bubble[(df_bubble.upload_date >= date_start) & (df_bubble.upload_date <= date_end)]
        df_bubble_grouped = df_bubble_sorted[[to_display,'sentiment','view_count','party']].groupby([to_display,'party']).agg({"sentiment": np.mean, 'view_count': np.sum}).reset_index()
        df_bubble_grouped  = df_bubble_grouped.sort_values('view_count', ascending = False)
        df_bubble_grouped = df_bubble_grouped[candidates_start:candidates_end]
        df_bubble_grouped['area'] = (df_bubble_grouped['view_count']/1e6)**3

        df = px.data.gapminder()
        fig = px.scatter(df_bubble_grouped, x="view_count", y="sentiment",
                    size="area", color="party",
                        hover_name=to_display, log_x=True, size_max=50,color_discrete_map= {'YSRCP': '#038d45','TDP': '#ffff00', 'JSP':'#f10003' })
        fig.update_layout(
            title='Constituency Graph',
            xaxis=dict(
                title='Views',
                gridcolor='white',
                type='log',
                gridwidth=2,
            ),
            yaxis=dict(
                title='Sentiment',
                gridcolor='white',
                gridwidth=2,
            )
        )
        col2.plotly_chart(fig,use_container_width=True )

        col_1,col_2 = st.columns(2)
        fig = px.bar(df_bubble_grouped, x=to_display, y="view_count",color='party', log_y=True, text_auto='.2s',color_discrete_map= {'YSRCP': '#038d45','TDP': '#ffff00', 'JSP':'#f10003' })
        fig.update_traces(marker_line_width=1.5, opacity=0.6)
        fig.update_layout(
            title='Constituency Graph',
            xaxis=dict(title=to_display),
            yaxis=dict(title='Views'))

        col_1.plotly_chart(fig)

        df_folium_plot = pd.read_csv('plots_data/dashboard_folium.csv')
        df_bubble = df_folium_plot[[to_display,'upload_date','sentiment','view_count','party']]
        df_bubble_grouped = df_bubble_sorted[[to_display,'sentiment','view_count','party']].groupby([to_display,'party']).agg({"sentiment": np.mean, 'view_count': np.sum}).reset_index()
        df_bubble_grouped  = df_bubble_grouped.sort_values('view_count', ascending = False)

        fig = px.treemap(df_bubble_grouped, path=[px.Constant("Parties"), 'party', to_display], values='view_count',
                        color='party', hover_data=['sentiment'],color_discrete_map= {'YSRCP': '#038d45','TDP': '#ffff00', 'JSP':'#f10003' })
        fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        fig.update_traces(marker=dict(cornerradius=5))
        col_2.plotly_chart(fig)

    def dashboard_get_tags_plot(self):

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
        <span class="word1">Andhra Pradesh </span>
        <span class="word2">Topics Distribution</span>
        </p>
        """, unsafe_allow_html=True)

        col1,col2 = st.columns([0.25,0.75])
        col1.write("##")
        col1.write("##")
        col1.write("##")
        col1.write("##")
        col1.write("##")

        col21, col22 = col1.columns(2)

        start_date = col21.date_input(
            "Start Date",
            datetime.date(2022, 1, 1), key='start date31')
        end_date = col22.date_input(
            "End Date",
            datetime.date(2024, 1, 1), key='start date32')
        date_start = str(start_date)
        date_end = str(end_date)
        total_tags_start, total_tags_end = col1.slider('Number of Topics',0, 150, (0, 10),key ='start date33')

        df_bar = self.df_tags_plot
        df_bar_sorted = df_bar[(df_bar.upload_date >= date_start) & (df_bar.upload_date <= date_end)]
        df_bar_grouped = df_bar_sorted.groupby(['tags']).agg({"sentiment": np.mean, 'view_count': np.sum, 'comment_count':np.sum,'duration':np.sum}).reset_index()
        df_bar_grouped  = df_bar_grouped.sort_values('view_count', ascending = False)
        df_bar_grouped = df_bar_grouped[total_tags_start:total_tags_end]
        df_bar_grouped['duration'] = df_bar_grouped['duration']/(60*60*24)
        df_bar_grouped['duration'] = np.round(df_bar_grouped['duration'],1)

        tags = df_bar_grouped['tags'].values
        views = df_bar_grouped['view_count'].values
        duration = df_bar_grouped['duration'].values


        y_saving = views
        y_net_worth  = duration
        x_saving = tags
        x_net_worth  = tags



        trace0 = go.Bar(
                        x=y_saving,
                        y=x_saving,
                        marker=dict(color='rgba(171, 50, 96, 0.6)',line=dict(color='rgba(171, 50, 96, 1.0)',width=1)),
                        name='Views',
                        orientation='h',
        )
        trace1 = go.Scatter(
                        x=y_net_worth,
                        y=x_net_worth,
                        mode='lines+markers',
                        line=dict(color='rgb(63, 72, 204)'),
                        name='Duration',
        )
        layout = dict(
                        title='Tags Views and Duration',
                        yaxis=dict(showticklabels=True,domain=[0, 0.85]),
                        yaxis2=dict(showline=True,showticklabels=False,linecolor='rgba(102, 102, 102, 0.8)',linewidth=2,domain=[0, 0.85]),
                        xaxis=dict(zeroline=False,showline=False,showticklabels=True,showgrid=True,domain=[0, 0.42]),
                        xaxis2=dict(zeroline=False,showline=False,showticklabels=True,showgrid=True,domain=[0.47, 1],side='top',dtick=25),
                        legend=dict(x=0.029,y=1.038,font=dict(size=10) ),
                        margin=dict(l=200, r=20,t=70,b=70),
        )
        annotations = []
        y_s = np.round(y_saving, decimals=2)
        y_nw = np.rint(y_net_worth)
        for ydn, yd, xd in zip(y_nw, y_s, x_saving):
            annotations.append(dict(xref='x2', yref='y2', y=xd, x=ydn - 4,text='{:,}'.format(ydn),font=dict(family='Arial', size=12),showarrow=False))
            annotations.append(dict(xref='x1', yref='y1', y=xd, x=yd + 3,text=str(yd),font=dict(family='Arial', size=12),showarrow=False))
        fig = tools.make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                                shared_yaxes=False, vertical_spacing=0.001)

        fig.append_trace(trace0, 1, 1)
        fig.append_trace(trace1, 1, 2)
        fig.update_layout(
            title='Constituency Graph',
            xaxis=dict(title='Views'),
            yaxis=dict(title='Tags'))
        fig['layout'].update(layout)
        col2.plotly_chart(fig, use_container_width = True)



        df_tags_plot = pd.read_csv('plots_data/dashboard_tags.csv')
        df_bar_grouped = df_tags_plot.groupby(['tags','uploader']).agg({"sentiment": np.mean, 'view_count': np.sum, 'comment_count':np.sum,'duration':np.sum}).reset_index()
        df_bar_grouped  = df_bar_grouped.sort_values('view_count', ascending = False)
        df_bar_grouped['duration'] = df_bar_grouped['duration']/(60*60*24)
        df_bar_grouped['duration'] = np.round(df_bar_grouped['duration'],1)


        fig = px.treemap(df_bar_grouped, path=[px.Constant("Media"), 'uploader', 'tags'], values='view_count',
                        color='uploader', hover_data=['duration','sentiment'],color_discrete_map= {'ABN': 'yellow','TV5': 'gold', 'Sakshi':'ff2a26' , 'TV9':'#0000FF'})
        fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        fig.update_traces(marker=dict(cornerradius=5))
        st.plotly_chart(fig, use_container_width = True)

                




