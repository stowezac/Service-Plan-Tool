import streamlit as st
import random

st.set_page_config(page_title="SSG Fox Full Tool", layout="wide")

# --- DATA INITIALIZATION ---
if 'init' not in st.session_state:
    st.session_state.init = True
    # PHQ-9
    for i in range(9): st.session_state[f"p{i}"] = "Not at all"
    # WEMWBS
    for i in range(14): st.session_state[f"w{i}"] = "Sometimes"
    # ISEL-12
    for i in range(12): st.session_state[f"i{i}"] = "Probably True"
    # SES LITERAL FIELDS FROM PDF
    st.session_state["ses_class"] = "Veteran"
    st.session_state["ses_income_src"] = []
    st.session_state["ses_emp_status"] = "Unemployed"
    st.session_state["ses_ft_pt"] = "NA"
    st.session_state["ses_job_loss"] = "Yes"
    st.session_state["ses_loss_time"] = "More than 1 Year"
    st.session_state["ses_unemp_ben"] = "No"
    st.session_state["ses_unemp_len"] = "Not applicable"
    st.session_state["ses_unemp_amt"] = "Not applicable"
    st.session_state["ses_tfa"] = "No"
    st.session_state["ses_counseling"] = "Yes"
    st.session_state["ses_difficulty"] = "Yes"
    st.session_state["ses_stress"] = "Yes"
    st.session_state["ses_total_inc"] = "$10,000 to $12,499"
    st.session_state["ses_inc_reduced"] = "Yes"
    st.session_state["ses_reduced_amt"] = "$30,000 to $34,999"
    st.session_state["ses_living"] = "Live with another Veteran"
    st.session_state["ses_area"] = "Urban"
    st.session_state["ses_edu"] = "Some college credit, but less than one year"

st.title("SSG Fox
