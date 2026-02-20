import streamlit as st
import random

st.set_page_config(page_title="SSG Fox Success Tool", layout="wide")

# --- DATA INITIALIZATION ---
if 'init' not in st.session_state:
    st.session_state.init = True
    # Standard Screeners
    for i in range(9): st.session_state[f"p{i}"] = "Not at all"
    for i in range(14): st.session_state[f"w{i}"] = "Sometimes"
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

st.title("SSG Fox Participant Success Tool")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9", "WEMWBS", "ISEL-12", "LITERAL SES FORM"])

with tab4:
    st.header("Socio-Economic Status (SES)")
    
    st.selectbox("Individual Classification", ["Veteran", "Active Duty Member", "Veteran Family Member", "Active Duty Family Member"], key="ses_class")
    
    st.multiselect("What are your regular sources of income?", 
                   ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement benefits", "Employment", "Temporary Financial Assistance", "All Other"], 
                   key="ses_income_src")
    
    st.selectbox("What is your current employment status?", ["Employed", "Unemployed", "Disabled", "Retired"], key="ses_emp_status")
    
    st.selectbox("Is it full-time or part-time?", ["Full-time", "Part-time", "NA"], key="ses_ft_pt")
    
    st.radio("Did you lose your job?", ["Yes", "No"], key="ses_job_loss")
    
    st.selectbox("Approximately how long ago did you lose your job?", ["0-6 Months", "6-12 Months", "More than 1 Year", "Not applicable"], key="ses_loss_time")
    
    st.radio("Are you receiving unemployment benefits?", ["Yes", "No"], key="ses_unemp_ben")
    
    st.selectbox("If yes, how long have you been receiving benefits?", ["Less than 6 Weeks", "6-14 Weeks", "15-26 Weeks", "Greater than 26 Weeks", "Not applicable"], key="ses_unemp_len")
    
    st.selectbox("How much are your weekly unemployment benefits?", ["$0.00-$99.99", "$100.00-$199.99", "$200.00-$299.99", "$300.00-$399.99", "$400.00-$499.99", "Not applicable"], key="ses_unemp_amt")
    
    st.radio("Are you receiving any temporary financial assistance?", ["Yes", "No", "Pending"], key="ses_tfa")
    
    st.radio("Have you ever received financial counseling services?", ["Yes", "No", "Pending"], key="ses_counseling")
    
    st.radio("Have you had difficulty covering medical, food, and housing expenses?", ["Yes", "No"], key="ses_difficulty")
    
    st.radio("Are you experiencing any stress over your financial situation?", ["Yes", "No"], key="ses_stress")
    
    st.selectbox("Total Household Income (Last 12 months)", ["Less than $5,000", "$5,000 to $7,499", "$10,000 to $12,499", "$20,000 to $24,999", "$50,000 or more"], key="ses_total_inc")
    
    st.radio("Has your income been reduced?", ["Yes", "No"], key="ses_inc_reduced")
    
    st.selectbox("How much has your income been reduced?", ["Less than $5,000", "$15,000 to $19,999", "$30,000 to $34,999", "Not applicable"], key="ses_reduced_amt")
    
    st.selectbox("What is your current living situation?", ["Live alone", "Live with spouse", "Live with another person", "Live with parents", "Live with another Veteran"], key="ses_living")
    
    st.selectbox("Which best describes the area you live in?", ["Urban", "Suburban", "Rural"], key="ses_area")
    
    st.selectbox("Highest grade level completed?", ["Less than high school", "High school diploma / GED", "Some college credit, but less than one year", "Bachelor's degree", "Master's degree"], key="ses_edu")

# --- LOGIC & REPORT ---
phq_score = sum([{"Not at all":0, "Several days":1, "More than half":2, "Nearly every day":3}[st.session_state[f"p{i}"]] for i in range(9)])

if st.button("Generate Tactical Service Plan"):
    st.divider()
    st.title("📋 Struggle Profile & Service Plan")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Risks")
        if st.session_state.ses_difficulty == "Yes": st.error("Difficulty covering Basic Needs")
        if st.session_state.ses_stress == "Yes": st.error("Financial Stress Detected")
        if st.session_state.p8 != "Not at all": st.error("Suicide Ideation Flagged (PHQ-9 Q9)")
        
    with col2:
        st.subheader("🛠️ Tactical Actions")
        if st.session_state.ses_emp_status == "Unemployed":
            st.write("👉 **VOCATIONAL:** Connect with DVOP/Workforce center.")
        if st.session_state.ses_counseling == "No":
            st.write("👉 **FINANCIAL:** Referral to financial counseling (Veteran has never received it).")
        if "VA Pension" not in st.session_state.ses_income_src:
            st.write("👉 **BENEFITS:** Peer to assist with VSO connection (No VA income reported).")
