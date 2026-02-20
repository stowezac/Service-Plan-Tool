import streamlit as st
import random

st.set_page_config(page_title="SSG Fox Tool", layout="wide")

# --- DATA INIT ---
if 'init' not in st.session_state:
    st.session_state.init = True
    for i in range(9): st.session_state[f"p{i}"] = "Not at all"
    for i in range(14): st.session_state[f"w{i}"] = "Sometimes"
    for i in range(12): st.session_state[f"i{i}"] = "Probably True"
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
    st.session_state["ses_edu"] = "Some college credit"

st.title("SSG Fox Participant Success Tool")

# --- TABS ---
t1, t2, t3, t4 = st.tabs(["PHQ-9", "WEMWBS", "ISEL-12", "SES (Literal PDF)"])

with t1:
    st.subheader("PHQ-9 Assessment")
    phq_qs = ["Little interest", "Feeling down", "Sleep issues", "No energy", "Appetite", "Failure", "Concentration", "Slow/Fidgety", "Self-harm"]
    for i, q in enumerate(phq_qs):
        st.radio(f"PHQ{i+1}: {q}", ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}")

with t2:
    st.subheader("WEMWBS Assessment")
    wem_qs = ["Optimistic", "Useful", "Relaxed", "Interested", "Energy", "Problems", "Clear thinking", "Self-worth", "Closeness", "Confident", "Loved", "Decisions", "New things", "Cheerful"]
    for i, q in enumerate(wem_qs):
        st.radio(f"WEM{i+1}: {q}", ["None", "Rarely", "Sometimes", "Often", "Always"], key=f"w{i}")

with t3:
    st.subheader("ISEL-12 Assessment")
    isel_qs = ["Trip help", "Private worries", "Chore help", "Family advice", "Movie buddy", "Problem advice", "Invites", "House sitter", "Lunch buddy", "Stranded help", "Crisis advice", "Moving help"]
    for i, q in enumerate(isel_qs):
        st.selectbox(f"ISEL{i+1}: {q}", ["Definitely False", "Probably False", "Probably True", "Definitely True"], key=f"i{i}")

with t4:
    st.header("Socio-Economic Status (SES)")
    # Mapped from provided PDF text
    st.selectbox("Select Individual Classification:", ["Active Duty Member", "Veteran", "Veteran Family Member", "Active Duty Family Member"], key="ses_class") # [cite: 7-9]
    st.multiselect("What are your regular sources of income?", ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement benefits", "Employment", "Temporary Financial Assistance", "All Other"], key="ses_income_src") # [cite: 10-22]
    st.selectbox("What is your current employment status?", ["Employed", "Unemployed", "Disabled", "Retired"], key="ses_emp_status") # [cite: 23-29]
    st.selectbox("Is it full-time or part-time?", ["Full-time", "Part-time", "NA"], key="ses_ft_pt") # [cite: 30-35]
    st.radio("Did you lose your job?", ["Yes", "No"], key="ses_job_loss") # [cite: 36-40]
    st.selectbox("How long ago did you lose your job?", ["0-6 Months", "6-12 Months", "More than 1 Year", "Not applicable"], key="ses_loss_time") # [cite: 42-50]
    st.radio("Are you receiving unemployment benefits?", ["Yes", "No"], key="ses_unemp_ben") # [cite: 51-55]
    st.selectbox("How long receiving unemployment?", ["Less than 6 Weeks", "6-14 Weeks", "15-26 Weeks", "Greater than 26 Weeks", "Not applicable"], key="ses_unemp_len") # [cite: 57-65]
    st.selectbox("Weekly benefit amount?", ["$0.00-$99.99", "$100.00-$199.99", "$200.00-$299.99", "$300.00-$399.99", "$400.00-$499.99", "Not applicable"], key="ses_unemp_amt") # [cite: 67-84]
    st.radio("Receiving any temporary financial assistance?", ["Yes", "No", "Pending"], key="ses_tfa") # [cite: 85-88]
    st.radio("Ever received financial counseling services?", ["Yes", "No", "Pending"], key="ses_counseling") # [cite: 89-93]
    st.radio("Difficulty covering medical, food, and housing?", ["Yes", "No"], key="ses_difficulty") # [cite: 94-97]
    st.radio("Experiencing stress over financial situation?", ["Yes", "No"], key="ses_stress") # [cite: 98-100]
    st.selectbox("Total Household Income (Last 12 months)", ["Less than $5,000", "$10,000 to $12,499", "$25,000 to $29,999", "$50,000 or more"], key="ses_total_inc") # [cite: 101-122]
    st.radio("Has your income been reduced?", ["Yes", "No"], key="ses_inc_reduced") # [cite: 123-127]
    st.selectbox("Current living situation?", ["Live alone", "Live with spouse", "Live with another person", "Live with parents", "Live with another Veteran"], key="ses_living") # [cite: 153-162]
    st.selectbox("Highest grade level/degree achieved?", ["Less than high school", "High school diploma / GED", "Some college credit", "Bachelor's degree", "Master's degree"], key="ses_edu") # [cite: 169-186]

# --- FINAL REPORT ---
if st.button("Generate Tactical Service Plan"):
    st.divider()
    st.title("📋 Tactical Service Plan")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🔴 Flagged Risks")
        if st.session_state.ses_difficulty == "Yes": st.error("Difficulty covering Basic Needs") # [cite: 94-95]
        if st.session_state.ses_stress == "Yes": st.error("Financial Stress Reported") # [cite: 98-100]
        if st.session_state.p8 != "Not at all": st.error("Suicide Ideation Flagged (PHQ-9 Q9)")
    with c2:
        st.subheader("🛠️ Immediate Actions")
        if st.session_state.ses_emp_status == "Unemployed":
            st.write("👉 **VOCATIONAL:** Connect with DVOP/Workforce center.") # [cite: 23-26]
        if st.session_state.ses_counseling == "No":
            st.write("👉 **FINANCIAL:** Referral to financial counseling.") # [cite: 89-92]
        if "VA Pension" not in st.session_state.ses_income_src and "Disability related income" not in st.session_state.ses_income_src:
            st.write("👉 **BENEFITS:** Assist with VSO connection (No VA income).") # [cite: 10-15]
