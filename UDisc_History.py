
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
from datetime import datetime
import pytz


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

custom_css = """
    <style>
        @media (max-width: 743px) {
            .laptop-table {
                display: none;
            }
        }
        @media (min-width: 744px) {
            .mobile-table {
                display: none;
            }
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

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
    individuals_data = ["-"] * length
    for individuals in rounds[date]:
        if individuals[0]==name:
            individuals_data = ["-" if x == 0 else int(x) for x in individuals[8:8+length]]
            return [individuals_data, int(individuals[5]), int(individuals[6])]
        else:
            pass
    return [individuals_data, "-", "-"]

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

def get_best(rounds, dates):
    names = ["Kav", "Nethidu", "Mahith"]
    pars = [int(x) for x in rounds[dates[0]][0][8:] if str(x) != 'nan']
    length = len(pars)
    all_data = {}
    for name in names:
        all_data[name] = None
        tries = []
        scores = []
        totals = []
        for date in dates:
            tries += [individuals_round(date, rounds, name, length)[0]]
            scores += [individuals_round(date, rounds, name, length)[2]]
            totals += [individuals_round(date, rounds, name, length)[1]]
        if totals.count("-") == len(totals):
            all_data[name] = [["-"] * length, '-', "-"]
        else:
            filtered_scores = [a for a in scores if a != "-"]
            filtered_totals = [a for a in totals if a != "-"]
            max_diff = max([x - y for x, y in zip(filtered_totals, filtered_scores)])
            valid_scores = []
            for i in range(len(filtered_scores)):
                if filtered_totals[i] - filtered_scores[i] == max_diff:
                    valid_scores += [filtered_scores[i]]
            min_score=min(valid_scores)
            for i in range(len(tries)):
                if scores[i] != "-":
                    if totals[i] - scores[i] == max_diff and scores[i]==min_score:
                        if all_data[name]==None:
                            all_data[name] = [tries[i], totals[i], scores[i]]
    return all_data


def laptop_style_table(df):
    
    df.columns = df.iloc[:2].values.tolist()  # Set the first two rows as headers
    df = df[2:].reset_index(drop=True)

    styled_df = df.style.set_table_styles([
        {"selector": "th, td", "props": [("font-size", "14px"), ("border", "none"), ("padding-right", "2px"), ("padding-left", "2px")]},
        {"selector": "thead th:first-child, tbody td:first-child", "props": [("text-align", "left")]},  # Align first column to the left
        {"selector": "th, td", "props": [("text-align", "center")]},  # Center align all other columns
        {"selector": "thead th", "props": [("border-bottom", "none")]},  # Remove horizontal border for header
        {"selector": "tbody td", "props": [("border-bottom", "none")]},  # Remove horizontal border for body
        {"selector": "th, td", "props": [("min-width", "32.61111111px")]},  # Apply min-width calculation
        ]).hide(axis="index").to_html()

    styled_html = f'<div class="laptop-table">{styled_df}</div>'

    return styled_html

def mobile_style_table(df):
    
    df.columns = df.iloc[:2].values.tolist()  # Set the first two rows as headers
    df = df[2:].reset_index(drop=True)

    styled_df = df.style.set_table_styles([
        {"selector": "th, td", "props": [("font-size", "14px"), ("border", "none"), ("padding-right", "2px"), ("padding-left", "2px")]},
        {"selector": "thead th:first-child, tbody td:first-child", "props": [("text-align", "left")]},  # Align first column to the left
        {"selector": "th, td", "props": [("text-align", "center")]},  # Center align all other columns
        {"selector": "thead th", "props": [("border-bottom", "none")]},  # Remove horizontal border for header
        {"selector": "tbody td", "props": [("border-bottom", "none")]},  # Remove horizontal border for body
        {"selector": "th, td", "props": [("min-width", "calc(min((11.111vw - 17.222px),(10vw - 10.4px)));")]},  # Apply min-width calculation
        ]).hide(axis="index").to_html()

    styled_html = f'<div class="mobile-table">{styled_df}</div>'

    return styled_html
    

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
        st.markdown(f"<p style='text-align: left; font-size: clamp(18px, 3.5vw, 26px); font-weight: bold;'>{current_course}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: left; font-size: clamp(14px, 2vw, 16px);'>⛳️&nbsp;&nbsp;{current_layout}</p>", unsafe_allow_html=True)

        # Given UTC time
        if date == "NA":
            pass
        else:
            utc_tz = pytz.timezone('UTC')
            nz_tz = pytz.timezone('Pacific/Auckland')
            utc_time = datetime.strptime(date, "%Y-%m-%d %H%M")
            utc_time = utc_tz.localize(utc_time)
            nz_time = utc_time.astimezone(nz_tz)
            formatted_date_time = "🗓️&nbsp;&nbsp;" + nz_time.strftime("%d/%m/%Y") + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🕒&nbsp;&nbsp;" + nz_time.strftime("%I:%M %p").lstrip("0")
            st.markdown(f"<p style='text-align: left; font-size: clamp(14px, 2vw, 16px);'>{formatted_date_time}</p>", unsafe_allow_html=True)

      # Create Columns
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        names = list(all_rounds_data.keys())[:3]  # Use dynamic player names if available

        # Display Player Data (Centered)
        for index, name in enumerate(names):
            with cols[index]:
                player_data = all_rounds_data.get(name, [0, 0, 0])  # Default values if missing
                score_display = f"{'+' if isinstance(player_data[2], int) and player_data[2] > 0 else ''}{player_data[2]} ({player_data[1]})"
                st.markdown(f"<p style='text-align: center; font-size: clamp(16px, 2.5vw, 18px); font-weight: bold;'>{name}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-size: clamp(14px, 2vw, 16px)'>{score_display}</p>", unsafe_allow_html=True)


        with st.expander("See hole data"):
            full_table = [["Hole"] + holes, ["Par"] + pars]
            for player in all_rounds_data:
                full_table.append([player] + all_rounds_data[player][0])
            df = pd.DataFrame(full_table)
            html_string = "<div>"
            html_string += laptop_style_table(df)
            if len(holes) > 9:
                first_table = [["Hole"] + holes[:9], ["Par"] + pars[:9]]
                second_table = [["Hole"] + holes[9:], ["Par"] + pars[9:]]
                for player in all_rounds_data:
                    first_table.append([player] + all_rounds_data[player][0][:9])
                    second_table.append([player] + all_rounds_data[player][0][9:])
                first_df = pd.DataFrame(first_table)
                second_df = pd.DataFrame(second_table)
                html_string += mobile_style_table(first_df)
                html_string += mobile_style_table(second_df)
            else:
                html_string += mobile_style_table(df)
            st.markdown(html_string+"</div>",unsafe_allow_html=True)

def main():
    data, course_layouts = fetch_data()
    Course = st.selectbox(
        "Select a course", list(course_layouts.keys()))

    Layout = st.selectbox(
        "Select a layout", course_layouts[Course])
    dates, rounds = get_all_rounds(data, course_layouts, Course, Layout)
    if Course != "All" and Layout != "All":
        all_rounds_data, holes, pars, current_course, current_layout = get_round(dates[0], rounds)
        best_rounds = get_best(rounds, dates)
        st.markdown(f"<p style='text-decoration: underline;margin-bottom: 0px; text-align: left; font-size: clamp(20px, 3.7vw, 28px); font-weight: bold;'>Personal Bests</p>", unsafe_allow_html=True)
        display_round(best_rounds, "NA", holes, pars, current_course, current_layout)
    st.markdown(f"<p style='text-decoration: underline;margin-bottom: 0px; text-align: left; font-size: clamp(20px, 3.7vw, 28px); font-weight: bold;'>Previous Rounds</p>", unsafe_allow_html=True)
    for date in dates:
        all_rounds_data, holes, pars, current_course, current_layout = get_round(date, rounds) 
        display_round(all_rounds_data, date, holes, pars, current_course, current_layout)

main()
