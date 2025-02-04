
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

with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Kav")
    with col2:
        st.write("Nethidu")
    with col3:
        st.write("Mahith")
with st.expander("See scores for each hole"):
    st.write("Data")
