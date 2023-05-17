from st_on_hover_tabs import on_hover_tabs
import streamlit as st
from PIL import Image
st.set_page_config(layout="wide")

_,col,_ = st.columns(3)
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)
logo = Image.open("logo.png").resize((60, 60))
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
    st.button('1')

elif tabs == 'Money':
    st.title("Paper")

elif tabs == 'Economy':
    st.title("Tom")