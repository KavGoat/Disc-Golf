
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

st.set_page_config(initial_sidebar_state="collapsed",
                   page_title="UDisc History")


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


def get_rounds(data, course_layouts, Course, Layout):
    dates = []
    for rounds in data:
        if Course == "All":
            date = rounds[3]
        elif Layout == "All":
            if rounds[1] == Course:
                date = rounds[3]
        elif rounds[1] == Course and rounds[2] == Layout:
            date = rounds[3]
        try:
            if date not in dates:
                dates += [date]
        except:
            pass
    dates.sort(reverse=True)
    rounds = {}
    
    for date in dates:
        ting = []
        for attempt in data:
            if attempt[3] == date:
                ting += [attempt]
        rounds[date] = ting
    return dates, rounds


data, course_layouts = fetch_data()
Course = st.selectbox(
    "Select a course", list(course_layouts.keys()))

Layout = st.selectbox(
    "Select a layout", course_layouts[Course])

date, rounds = get_rounds(data, course_layouts, Course, Layout)
for roundt in list(rounds.keys()):
    st.write(rounds[roundt][0][3])
    st.write(roundt)
