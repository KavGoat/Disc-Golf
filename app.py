
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
        return data.reset_index().values.tolist()
    except:
        pass

tab1, tab2 = st.tabs(["Scores", "Update Data"])

y=0

with tab1:

    ting = np.arange(y)

    for x in ting:
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
                st.write("Data")

with tab2:
    data = fetch_data()
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        dates1 = []
        
        for tingle in data:
            if isinstance(tingle[3], str) and tingle[3] not in dates1:
                dates1 += [tingle[3]]
  
        dfd = pd.read_csv(uploaded_file)
        
        new_data = dfd.reset_index().values.tolist()
        
        
        data_to_append = []
            
        for ting1 in new_data:
            if ting1[4] not in dates1 and isinstance(ting1[4], str):
                data_to_append += [ting1[1:]]
        
        append_clean = [
            [None if isinstance(x, float) and math.isnan(x) else x for x in row]
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
        credentials = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
            
        gc = gspread.authorize(credentials)
            
        sh = gc.open_by_key("1M4VT4eXXPj5UL7Xn8s5B1yu_taULnGQ3jHKzmG14rIA")
            
        sheet = sh.worksheet("Data")
            
            
            # Append data to the end of the sheet
        f = StringIO()
        with redirect_stdout(f):
            
            sheet.append_rows(append_clean, value_input_option="USER_ENTERED")