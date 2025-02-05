
import streamlit as st
import pandas as pd
import numpy as np
import ssl
from io import StringIO
import gspread
from google.oauth2.service_account import Credentials
import sys
from contextlib import redirect_stdout
import math
import os

st.set_page_config(initial_sidebar_state="collapsed", page_title="UDisc History")


st.markdown("""
    <style>
    
           /* Remove blank space at top and bottom */ 
           .stMainBlockContainer {
               padding-top: 3rem;
               padding-left: 1rem;
               padding-right: 1rem;
               padding-bottom: 10rem;
            }
    </style>
    """, unsafe_allow_html=True)

def fetch_data():
    try:
        data = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                           '1M4VT4eXXPj5UL7Xn8s5B1yu_taULnGQ3jHKzmG14rIA' +
                           '/export?gid=0&format=csv',
                           index_col=0
                           )
        data = data.reset_index().values.tolist()
        courses = []
        for round in data:
            if round[1] not in courses:
                courses.append(round[1])

        course_layouts = {"All": "-"}

        for course in courses:
            layouts = []
            for round in data:
                if round[1] == course and round[2] not in layouts:
                    layouts.append(round[2])
            if len(layouts) > 1:
                layouts = ["All"] + layouts
            course_layouts[course] = layouts
        return data, course_layouts
    except:
        pass


data, course_layouts = fetch_data()
Course = st.selectbox(
    "Select a course", list(course_layouts.keys()))

Layout = st.selectbox(
    "Select a layout", course_layouts[Course])

"""for x in ting:
        with st.container(border=True):
            st.write(str(x))
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("Kav")
            with col2:
                st.write("Nethidu")
            with col3:
                st.write("Mahith")
            with st.expander("See scores for each hole"):
                st.write("Data")"""
