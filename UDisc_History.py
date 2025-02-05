
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


def get_all_rounds(data, course_layouts, Course, Layout):
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

def individuals_round(date, rounds, name, length):
    for individuals in rounds[date]:
        if individuals[0]==name:
            individuals_data = ["-" if x == 0 else int(x) for x in individuals[8:8+length]]
            return [individuals_data, int(individuals[5]), int(individuals[6])]
        else:
            pass

def get_round(date, rounds):
    names = ["Kav", "Nethidu", "Mahith"]
    par_score = int(rounds[date][0][5])
    pars = [int(x) for x in rounds[date][0][8:] if str(x) != 'nan']
    length = len(pars)
    holes = list(range(1, length + 1))
    all_rounds_data = {}
    current_course=rounds[date][0][1]
    current_layout=rounds[date][0][2]
    for name in names:
        all_rounds_data[name]=individuals_round(date, rounds, name, length)
    return all_rounds_data, holes, pars, current_course, current_layout


def display_round(all_rounds_data, date, holes, pars, current_course, current_layout):
    st.markdown("""
        <style>
            .stHorizontalBlock {
                display: flex;
                flex-wrap: nowrap;
            }
            .stHorizontalBlock .stColumn {
                width: calc(33.3333333% - 1rem); /* Adjust width */
                min-width: unset;               /* Unset min-width */
            }
        </style>
    """, unsafe_allow_html=True)
    with st.container(border=True):
        # Display Course and Layout (Left-Aligned)
        st.markdown(f"<p style='text-align: left; font-size: 26px; font-weight: bold;'>{current_course}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: left; font-size: 16px;'>{current_layout}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: left; font-size: 16px;'>{date}</p>", unsafe_allow_html=True)

      # Create Columns
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        names = list(all_rounds_data.keys())[:3]  # Use dynamic player names if available

        # Display Player Data (Centered)
        for index, name in enumerate(names):
            with cols[index]:
                player_data = all_rounds_data.get(name, [0, 0, 0])  # Default values if missing
                score_display = f"{'+' if player_data[2] > 0 else ''}{player_data[2]} ({player_data[1]})"
                
                st.markdown(f"<p style='text-align: center; font-size: 18px; font-weight: bold;'>{name}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-size: 16px;'>{score_display}</p>", unsafe_allow_html=True)

        # Expander for hole data (Left-Aligned)
        with st.expander("See hole data"):
            st.markdown("<p style='text-align: left; font-size: 14px;'>Test</p>", unsafe_allow_html=True)


def main():
    data, course_layouts = fetch_data()
    Course = st.selectbox(
        "Select a course", list(course_layouts.keys()))

    Layout = st.selectbox(
        "Select a layout", course_layouts[Course])

    dates, rounds = get_all_rounds(data, course_layouts, Course, Layout)
    for date in dates:
        all_rounds_data, holes, pars, current_course, current_layout = get_round(date, rounds)
        display_round(all_rounds_data, date, holes, pars, current_course, current_layout)

main()
    
