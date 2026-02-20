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

st.title("SSG Fox Participant Success Tool")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9", "WEMWBS", "ISEL-12", "SES (Literal PDF)"])

with tab1:
    st.subheader("PHQ-9: Mood Assessment")
    phq_q = ["Little interest or pleasure", "Feeling down, depressed, hopeless", "Trouble sleeping", "Feeling tired/little energy", "Poor appetite/overeating", "Feeling like a failure", "Trouble concentrating", "Moving slowly/Fidgety", "Thoughts of self-harm"]
    for i, q in enumerate(phq_q):
        st.radio(f"PHQ{i+1}: {q}", ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}")

with tab2:
    st.subheader("WEMWBS: Mental Well-being")
    wem_q = ["Optimistic", "Useful", "Relaxed", "Interested in people", "Energy", "Problem solving", "Thinking clearly", "Self-worth", "Closeness", "Confidence", "Loved", "Decision making", "New things", "Cheerful"]
    for i, q in enumerate(wem_q):
        st.radio(f"WEM{i+1}: {q}", ["None", "Rarely", "Sometimes", "Often", "Always"], key=f"w{i}")

with tab3:
    st.subheader("ISEL-12: Social Support")
    isel_items = ["I’d have a hard time finding someone to go on a trip with me.", "There is no one I can share my most private worries with.", "If I were sick, I could easily find help with chores.", "I have someone to turn to for advice about family problems.", "I could easily find someone to go to a movie with.", "When I need suggestions for a personal problem, I have someone to turn to.", "I don’t often get invited to do things with others.", "If I went out of town, someone would look after my house.", "If I wanted lunch, I could easily find someone to join me.", "If I was stranded, someone would come and get me.", "If a crisis arose, it would be hard to find advice.", "If I needed help moving, I’d have a hard time finding help."]
    for i, q in enumerate(isel_items):
        st.selectbox(q, ["Definitely False", "Probably False", "Probably True", "Definitely True"], key=f"i{i}")

with tab4:
    st.header("Socio-Economic Status (Literal Map)")
    # Exactly matching PDF sequence
    st.selectbox("Select Individual Classification:", ["Veteran", "Active Duty Member", "Veteran Family Member", "Active Duty Family Member"], key="ses_class") #
    st.multiselect("What are your regular sources of income? [SELECT ALL THAT APPLY]", ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement benefits", "Employment", "Temporary Financial Assistance", "All Other"], key="ses_income_src") #
    st.selectbox("What is your current employment status? [SELECT ONE]", ["Employed", "Unemployed", "Disabled", "Retired"], key="ses_emp_status") #
    st.selectbox("Is it full-time or part-time? [SELECT ONE]", ["Full-time", "Part
