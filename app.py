
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

ssl._create_default_https_context = ssl._create_unverified_context

st.markdown('<style>.stSelectbox > div { width: 100% !important; }</style>', unsafe_allow_html=True)
st.markdown('<style>.stMarkdownContainer > div { width: 100% !important; }</style>', unsafe_allow_html=True)
st.markdown("""
    <style>
    
           /* Remove blank space at top and bottom */ 
           .block-container {
               padding-top: 1rem;
               padding-bottom: 1rem;
            }

    </style>
    """, unsafe_allow_html=True)

# Function to fetch data
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
data = fetch_data()
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
    # Dropdowns with session state
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
        data = fetch_data()
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
Course = st.selectbox(
    "Select a course", list(course_layouts.keys()), key="selected_course"
)
        
Layout = st.selectbox(
    "Select a layout", course_layouts[Course], key="selected_layout"
)
    

def rest(Course, Layout):
        global data
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
        htmlting = ""
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
            for go in data:
                if go[3] == date:
                    ting += [go]
            rounds[date] = ting
    
        rounds_data = {}
        for key in rounds.keys():
            pars = []
            for hole in rounds[key][0][8:]:
                if not np.isnan(hole):
                    pars += [int(hole)]
            holes = len(pars)
    
            kavs = []
            nethidus = []
            mahiths = []
            rounds_data[key] = []
            for go in rounds[key]:
                if go[0] == "Kav":
                    kav_total = go[5]
                    kav_score = go[6]
                    for hole in go[8:]:
                        if not np.isnan(hole):
                            if hole != 0:
                                kavs += [int(hole)]
                            else:
                                kavs += ["-"]
                if go[0] == "Nethidu":
                    net_total = go[5]
                    net_score = go[6]
                    for hole in go[8:]:
                        if not np.isnan(hole):
                            if hole != 0:
                                nethidus += [int(hole)]
                            else:
                                nethidus += ["-"]
                if go[0] == "Mahith":
                    mah_total = go[5]
                    mah_score = go[6]
                    for hole in go[8:]:
                        if not np.isnan(hole):
                            if hole != 0:
                                mahiths += [int(hole)]
                            else:
                                mahiths += ["-"]
            if len(kavs) == 0:
                kavs = ["Kav"] + ["-"] * (len(pars) + 2)
            else:
                kavs = ["Kav"] + kavs + [int(kav_total), int(kav_score)]
            if len(nethidus) == 0:
                nethidus = ["Nethidu"] + ["-"] * (len(pars) + 2)
            else:
                nethidus = ["Nethidu"] + nethidus + [int(net_total), int(net_score)]
            if len(mahiths) == 0:
                mahiths = ["Mahith"] + ["-"] * (len(pars) + 2)
            else:
                mahiths = ["Mahith"] + mahiths + [int(mah_total), int(mah_score)]
    
            header = ["Hole"] + list(range(1, len(pars) + 1)) + ["Total", "+/-"]
            pars = ["Par"] + pars + [sum(pars), "-"]
            round_data = [header, pars, kavs, nethidus, mahiths]
            rounds_data[key] += round_data
    
        try:
            if not (Course == "All" or Layout == "All"):
                kav_datas = []
                net_datas = []
                mah_datas = []
                for key in rounds_data.keys():
                    kav_score = rounds_data[key][2][-1]
                    net_score = rounds_data[key][3][-1]
                    mah_score = rounds_data[key][4][-1]
    
                    if kav_score == "-":
                        kav_datas += [[key, "-", "-"]]
                    else:
                        kav_datas += [[key, kav_score, rounds_data[key][2][-2] - kav_score]]
                    if net_score == "-":
                        net_datas += [[key, "-", "-"]]
                    else:
                        net_datas += [[key, net_score, rounds_data[key][3][-2] - net_score]]
                    if mah_score == "-":
                        mah_datas += [[key, "-", "-"]]
                    else:
                        mah_datas += [[key, mah_score, rounds_data[key][4][-2] - mah_score]]
    
                header = rounds_data[list(rounds_data.keys())[0]][0]
                pars = rounds_data[list(rounds_data.keys())[0]][1]
    
                kav_valid = False
                for plays in kav_datas:
                    if plays[-1] != "-":
                        kav_valid = True
    
                net_valid = False
                for plays in net_datas:
                    if plays[-1] != "-":
                        net_valid = True
    
                mah_valid = False
                for plays in mah_datas:
                    if plays[-1] != "-":
                        mah_valid = True
    
                if kav_valid:
                    max_kav_total = 0
                    for plays in kav_datas:
                        if plays[-1] != "-":
                            max_kav_total = max(max_kav_total, plays[-1])
                    valid_kav_scores = []
                    for plays in kav_datas:
                        if plays[-1] == max_kav_total:
                            valid_kav_scores += [plays[-2]]
                    best_kav = float("inf")
                    kav_key = ""
                    for valid_score in valid_kav_scores:
                        best_kav = min(best_kav, valid_score)
                    for plays in kav_datas:
                        if plays[-2] == best_kav:
                            kav_key = plays[0]
                else:
                    kav_key = list(rounds_data.keys())[0]
    
                if net_valid:
                    max_net_total = 0
                    for plays in net_datas:
                        if plays[-1] != "-":
                            max_net_total = max(max_net_total, plays[-1])
                    valid_net_scores = []
                    for plays in net_datas:
                        if plays[-1] == max_net_total:
                            valid_net_scores += [plays[-2]]
                    best_net = float("inf")
                    net_key = ""
                    for valid_score in valid_net_scores:
                        best_net = min(best_net, valid_score)
                    for plays in net_datas:
                        if plays[-2] == best_net:
                            net_key = plays[0]
                else:
                    net_key = list(rounds_data.keys())[0]
    
                if mah_valid:
                    max_mah_total = 0
                    for plays in mah_datas:
                        if plays[-1] != "-":
                            max_mah_total = max(max_mah_total, plays[-1])
                    valid_mah_scores = []
                    for plays in mah_datas:
                        if plays[-1] == max_mah_total:
                            valid_mah_scores += [plays[-2]]
                    best_mah = float("inf")
                    mah_key = ""
                    for valid_score in valid_mah_scores:
                        best_mah = min(best_mah, valid_score)
                    for plays in mah_datas:
                        if plays[-2] == best_mah:
                            mah_key = plays[0]
                else:
                    mah_key = list(rounds_data.keys())[0]
    

                htmlting += """<p><strong style="text-decoration: underline; font-size: min(22px,3.5vw);">Personal Bests</strong></p>"""
                df2 = pd.DataFrame([rounds_data[kav_key][2],rounds_data[net_key][3],rounds_data[mah_key][4]], columns=pd.MultiIndex.from_tuples(zip(header, pars)))
                gap_row = pd.Series([""] * len(df2.columns), index=df2.columns)
                df2.loc[-1] = gap_row
                df2.index = df2.index + 1  # Shift the index
                df2 = df2.sort_index()
                styled_df2 = df2.style.set_table_styles([
                    {'selector': 'table', 'props': [('font-size', 'min(17px,2.8vw)')]},  # Set font size for the entire table
                    {'selector': 'th, td', 'props': [('min-width', 'min(31.8px,4.14vw)'), ('font-size', 'min(17px,2.8vw)')]},  # Apply font size to all cells explicitly
                    {'selector': 'td', 'props': [('text-align', 'center'), ('font-size', 'min(17px,2.8vw)')]},  # Center-align and set font size for data cells
                    {'selector': 'th:nth-child(1)', 'props': [('font-weight', 'bold'), ('text-align', 'left'), ('font-size', 'min(17px,2.8vw)')]},  # Bold and left-align the first column header
                    {'selector': 'td:nth-child(1)', 'props': [('font-weight', 'bold'), ('text-align', 'left'), ('font-size', 'min(17px,2.8vw)')]},  # Bold and left-align the first column data cells
                    {'selector': 'th', 'props': [('text-align', 'center'), ('font-weight', 'normal'), ('font-size', 'min(17px,2.8vw)')]},  # Center-align all headers, unbold, and set font size
                    {'selector': 'td:nth-child(n+2)', 'props': [('font-weight', 'normal'), ('font-size', 'min(17px,2.8vw)')]},  # Ensure no bolding and apply font size for non-first columns
                    {'selector': 'th, td', 'props': [('padding', '0.1em')]},
                    {'selector': 'table, th, td', 'props': [('border', '0px solid transparent')]} 
                ], overwrite=False).hide(axis="index")
                htmlting += str(styled_df2.to_html())
                htmlting += """<hr style="height: 0px; border: none; background-color: none; margin-top: 15px; margin-bottom: 15px;">"""
            else:
                pass
        except:
            pass
    
        htmlting += """<p><strong style="text-decoration: underline; font-size: min(22px,3.5vw);">Previous Rounds</strong></p>"""
        for key in rounds_data.keys():
            kav_score = rounds_data[key][2][-1]
            net_score = rounds_data[key][3][-1]
            mah_score = rounds_data[key][4][-1]
    
            winners = []
    
            # Filter out "-" scores and find the minimum of the remaining valid scores
            valid_scores = []
    
            if kav_score != "-":
                valid_scores.append(("Kav", kav_score))
            if net_score != "-":
                valid_scores.append(("Nethidu", net_score))
            if mah_score != "-":
                valid_scores.append(("Mahith", mah_score))
    
            # Check if there is only one valid score
            if len(valid_scores) == 1:
                winner = "-"
            else:
                # If there are valid scores, find the minimum
                if valid_scores:
                    min_score = min(score for name, score in valid_scores)
    
                    # Compare and append the winner(s)
                    for name, score in valid_scores:
                        if score == min_score:
                            winners.append(name)
    
                # Convert the list of winners to a string
                winner = " and ".join(winners)
    
            if not (Course == "All" or Layout == "All"):
                head_ting = [["Winner", winner]]
            elif Layout == "All":
                head_ting = [["Layout", rounds[key][0][2]], ["Winner", winner]]
            else:
                head_ting = [["Course", rounds[key][0][1]], ["Layout", rounds[key][0][2]], ["Winner", winner]]
    
            
            df1 = pd.DataFrame(head_ting, columns=["Date", key])
            styled_df1 = df1.style.set_properties(**{'text-align': 'left', 'font-size': 'min(17px,2.8vw))'}) \
                .set_table_styles([
                    {
                        'selector': 'th',
                        'props': [('font-weight', 'normal'), ('text-align', 'left'), ('font-size', 'min(17px,2.8vw)')]  # Default style for headers
                    },
                    {
                        'selector': 'th:nth-child(1)',
                        'props': [('font-weight', 'bold'), ('font-size', 'min(17px,2.8vw)')]  # Bold the first column header
                    },
                    {
                        'selector': 'td:nth-child(1)',
                        'props': [('font-weight', 'bold'), ('font-size', 'min(17px,2.8vw)')]  # Bold the first column cells
                    },
                    {
                        'selector': 'td',
                        'props': [('text-align', 'left'), ('font-size', 'min(17px,2.8vw)'), ('padding', '0.1em')]  # Left-align, set font size, and add padding to data cells
                    },
                    {
                        'selector': 'table',
                        'props': [('border-collapse', 'collapse'), ('font-size', 'min(17px,2.8vw)')]  # Ensure borders collapse and set font size for table
                    },
                    {
                        'selector': 'tr:nth-child(odd)',
                        'props': [('background-color', 'transparent'), ('font-size', 'min(17px,2.8vw)')]  # Remove alternating background colors for odd rows
                    },
                    {
                        'selector': 'tr:nth-child(even)',
                        'props': [('background-color', 'transparent'), ('font-size', 'min(17px,2.8vw)')]  # Remove alternating background colors for even rows
                    },
                    {
                        'selector': 'td:nth-child(n+2)',
                        'props': [('font-weight', 'normal'), ('font-size', 'min(17px,2.8vw)')]  # Ensure no bolding and set font size for non-first columns
                    },
                    {
                        'selector': 'th, td',
                        'props': [('padding', '0.1em')]  # Add padding to all header and data cells
                    },
                    {'selector': 'table, th, td', 'props': [('border', '0px solid transparent')]} 
                ], overwrite=False).hide(axis="index")
    
            htmlting += str(styled_df1.to_html())
    
            
            round_data = rounds_data[key]
            df = pd.DataFrame(round_data[2:], columns=pd.MultiIndex.from_tuples(zip(round_data[0], round_data[1])))
            gap_row = pd.Series([""] * len(df.columns), index=df.columns)
            df.loc[-1] = gap_row
            df.index = df.index + 1  # Shift the index
            df = df.sort_index()
            styled_df = df.style.set_table_styles([
                {'selector': 'table', 'props': [('font-size', 'min(17px,2.8vw)')]},  # Set font size for the entire table
                {'selector': 'th, td', 'props': [('min-width', 'min(31.8px,4.13vw)'), ('font-size', 'min(17px,2.8vw)')]},  # Apply font size to all cells explicitly
                {'selector': 'td', 'props': [('text-align', 'center'), ('font-size', 'min(17px,2.8vw)')]},  # Center-align and set font size for data cells
                {'selector': 'th:nth-child(1)', 'props': [('font-weight', 'bold'), ('text-align', 'left'), ('font-size', 'min(17px,2.8vw)')]},  # Bold and left-align the first column header
                {'selector': 'td:nth-child(1)', 'props': [('font-weight', 'bold'), ('text-align', 'left'), ('font-size', 'min(17px,2.8vw)')]},  # Bold and left-align the first column data cells
                {'selector': 'th', 'props': [('text-align', 'center'), ('font-weight', 'normal'), ('font-size', 'min(17px,2.8vw)')]},  # Center-align all headers, unbold, and set font size
                {'selector': 'td:nth-child(n+2)', 'props': [('font-weight', 'normal'), ('font-size', 'min(17px,2.8vw)')]},  # Ensure no bolding and apply font size for non-first columns
                {'selector': 'th, td', 'props': [('padding', '0.1em')]},
                {'selector': 'table, th, td', 'props': [('border', '0px solid transparent')]} 
            ], overwrite=False).hide(axis="index")
    
    
    
    
            table_html = styled_df.to_html()
            
            # Append to the final HTML
            htmlting += str(table_html)
            htmlting += """<hr style="height: 0px; border: none; background-color: none; margin-top: 15px; margin-bottom: 15px;">"""
        st.markdown(htmlting, unsafe_allow_html=True)       

if Course and Layout and Layout in  course_layouts[Course]:
    rest(Course, Layout)

    
