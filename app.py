
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

def update_data():
    st.markdown("""
    <script>
        document.getElementById('tabs-bui2-tab-0').setAttribute('aria-selected','True');
        document.getElementById('tabs-bui2-tab-1').setAttribute('aria-selected','False');
        document.getElementById('tabs-bui2-tabpanel-1').setAttribute('hidden','');
        document.getElementById('tabs-bui2-tabpanel-0').removeAttribute('hidden','False');
    </script>
    """, unsafe_allow_html=True)
    st.rerun()

tab1, tab2 = st.tabs(["Scores", "Update Data"])

with tab1:
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

with tab2:
    data,course_layouts = fetch_data()
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        dates = []
        for tingle in data:
            if isinstance(tingle[3], str) and tingle[3] not in dates:
                dates += [tingle[3]]

        dfd = pd.read_csv(uploaded_file)

        new_data = dfd.reset_index().values.tolist()

        data_to_append = []

        for ting1 in new_data:
            if ting1[4] not in dates and isinstance(ting1[4], str):
                data_to_append += [ting1[1:]]

        append_clean = [
            [None if isinstance(x, float) and math.isnan(x)
             else x for x in row]
            for row in data_to_append
        ]

        SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials_info = {
            "type": "service_account",
            "project_id": "udisc-448721",
            "private_key_id": st.secrets["gapi"]["gapi_id"],
            "private_key": st.secrets["gapi"]["gapi_key"],
            "client_email": "udisc-790@udisc-448721.iam.gserviceaccount.com",
            "client_id": "108793919915702574689",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/udisc-790%40udisc-448721.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }
        credentials = Credentials.from_service_account_info(
            credentials_info, scopes=SCOPES)

        gc = gspread.authorize(credentials)

        sh = gc.open_by_key("1M4VT4eXXPj5UL7Xn8s5B1yu_taULnGQ3jHKzmG14rIA")

        sheet = sh.worksheet("Data")

        # Append data to the end of the sheet
        f = StringIO()
        with redirect_stdout(f):

            sheet.append_rows(append_clean, value_input_option="USER_ENTERED")
        st.link_button("Update", "https://udiscgolf.streamlit.app/")
