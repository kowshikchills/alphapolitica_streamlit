from st_on_hover_tabs import on_hover_tabs
import streamlit as st
from PIL import Image
from dashboard import *
from profile_page import *

st.set_page_config(layout="wide")

_,col,_ = st.columns(3)
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)
logo = Image.open("netra.png").resize((60, 60))
st.sidebar.image(logo,)
st.sidebar.header(' ')

with st.sidebar:
        tabs = on_hover_tabs(tabName=['Dashboard', 'Profile Analysis', 'Issue Analysis', 'Counter'], 
                             iconName=['dashboard', 'query_stats', 'visibility', 'sports_gymnastics'],
                             styles = {'navtab': {'background-color':'#111',
                                                  'color': '#048d46',
                                                  'font-size': '18px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap'},
                                       'tabOptionsStyle': {':hover :hover': {'color': '#0565b5',
                                                                      'cursor': 'pointer'}},
                                       'iconStyle':{'position':'fixed',
                                                    'left':'7.5px',
                                                    'text-align': 'left'},
                                       'tabStyle' : {'list-style-type': 'none',
                                                     'margin-bottom': '30px',
                                                     'padding-left': '30px'}},
                             key="1",default_choice=0)

if tabs =='Dashboard':
    DB = Dashboard()
    DB.dashboard_show_folium_map()
    DB.dashboard_create_data_uploader_charts()
    DB.dashboard_show_uploader_chart()
    DB.dashboard_show_constituency_plots()
    DB.dashboard_get_tags_plot()

elif tabs == 'Profile Analysis':
    PP = ProfilePage()
    PP.get_overall_chart()



elif tabs == 'Economy':
    st.title("Tom")