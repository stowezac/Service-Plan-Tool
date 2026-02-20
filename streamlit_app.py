import streamlit as st
import random

st.set_page_config(page_title="SSG Fox Participant Tool", layout="wide")

# --- DATA SYSTEM ---
if 'init' not in st.session_state:
    st.session_state.init = True
    for i in range(9): st.session_state[f"p{i}"] = "Not at all"
    for i in range(14): st.session_state[f"w{i}"] = "Sometimes"
    for i in range(12): st.session_state[f"i{i}"] = "Probably True"
    st.session_state["ses_class"] = "Veteran"
    st.session_state["ses_income_src"] = ["Disability related income"]
    st.session_state["ses_emp_status"] = "Unemployed"
    st.session_state["ses_ft_pt"] = "NA"
    st.session_state["ses_job_loss"] = "Yes"
    st.session_state["ses_loss_time"] = "More than 1 Year"
    st.session_state["ses_unemp_ben"] = "No"
    st.session_state["ses_unemp_len"] = "Not applicable"
    st.session_state["ses_unemp_amt"] = "Not applicable"
    st.session_state["ses_tfa"] = "No"
    st.session_state["ses_counseling"] = "No"
    st.session_state["ses_difficulty"] = "Yes"
    st.session_state["ses_stress"] = "Yes"
    st.session_state["ses_total_inc"] = "$10,000 to $12,499"
    st.session_state["ses_inc_reduced"] = "No"
    st.session_state["ses_reduced_amt"] = "Not applicable"
    st.session_state["ses_living"] = "Live with another Veteran"
    st.session_state["ses_area"] = "Urban"
    st.session_state["ses_edu"] = "Some college credit, but less than one year of college credit"

def fill_random():
    for i in range(9): st.session_state[f"p{i}"] = random.choice(["Not at all", "Several days", "More than half", "Nearly every day"])
    for i in range(14): st.session_state[f"w{i}"] = random.choice(["None", "Rarely", "Sometimes", "Often", "Always"])
    for i in range(12): st.session_state[f"i{i}"] = random.choice(["Definitely False", "Probably False", "Probably True", "Definitely True"])
    st.session_state["ses_difficulty"] = random.choice(["Yes", "No"])
    st.session_state["ses_stress"] = random.choice(["Yes", "No"])
    st.session_state["ses_emp_status"] = random.choice(["Employed", "Unemployed", "Disabled", "Retired"])

st.title("SSG Fox Participant Success Tool")
st.button("🎲 Randomize All Forms", on_click=fill_random)

tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9", "WEMWBS", "ISEL-12", "SES (Literal PDF Flow)"])

# ... [PHQ-9, WEMWBS, ISEL-12 inputs remain same as previous literal versions] ...
with tab1:
    phq_q = ["Little interest or pleasure in doing things", "Feeling down, depressed, or hopeless", "Trouble falling or staying asleep, or sleeping too much", "Feeling tired or having little energy", "Poor appetite or overeating", "Feeling bad about yourself — or that you are a failure or have let yourself or your family down", "Trouble concentrating on things, such as reading the newspaper or watching television", "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual", "Thoughts that you would be better off dead or of hurting yourself in some way"]
    for i, q in enumerate(phq_q): st.radio(f"PHQ{i+1}: {q}", ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}")

with tab2:
    wem_q = ["I've been feeling optimistic about the future", "I've been feeling useful", "I've been feeling relaxed", "I've been feeling interested in other people", "I've been having energy to spare", "I've been dealing with problems well", "I've been thinking clearly", "I've been feeling good about myself", "I've been feeling close to other people", "I've been feeling confident", "I've been able to make up my own mind about things", "I've been feeling loved", "I've been interested in new things", "I've been feeling cheerful"]
    for i, q in enumerate(wem_q): st.radio(f"WEM{i+1}: {q}", ["None", "Rarely", "Sometimes", "Often", "Always"], key=f"w{i}")

with tab3:
    isel_items = ["If I wanted to go on a trip for a day...", "There is no one I can share my most private worries...", "If I were sick, I could easily find help...", "There is someone I can turn to for advice...", "I could easily find someone to go to a movie...", "When I need suggestions on how to deal with a personal problem...", "I don't often get invited to do things...", "If I had to go out of town...", "If I wanted to have lunch with someone...", "If I was stranded 10 miles from home...", "If a crisis arose in my life...", "If I were moving..."]
    for i, q in enumerate(isel_items): st.selectbox(q, ["Definitely False", "Probably False", "Probably True", "Definitely True"], key=f"i{i}")

with tab4:
    st.header("Socio-Economic Status (Literal Map)")
    st.selectbox("Select Individual Classification:", ["Active Duty Member", "Veteran", "Veteran Family Member", "Active Duty Family Member"], key="ses_class")
    st.multiselect("What are your regular sources of income?", ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement benefits", "Employment", "Temporary Financial Assistance", "All Other"], key="ses_income_src")
    st.selectbox("What is your current employment status?", ["Employed", "Unemployed", "Disabled", "Retired"], key="ses_emp_status")
    st.selectbox("Is it full-time or part-time?", ["Full-time", "Part-time", "NA"], key="ses_ft_pt")
    st.radio("Did you lose your job?", ["Yes", "No"], key="ses_job_loss")
    st.selectbox("Approximately how long ago did you lose your job?", ["0-6 Months", "6-12 Months", "More than 1 Year", "Not applicable"], key="ses_loss_time")
    st.radio("Are you receiving unemployment benefits?", ["Yes", "No"], key="ses_unemp_ben")
    st.radio("Have you ever received financial counseling services?", ["Yes", "No", "Pending"], key="ses_counseling")
    st.radio("Have you had difficulty covering medical, food, and housing expenses?", ["Yes", "No"], key="ses_difficulty")
    st.radio("Are you experiencing any stress over your financial situation?", ["Yes", "No"], key="ses_stress")
    st.selectbox("Total Household Income (Last 12 months)", ["Less than $5,000", "$10,000 to $12,499", "$50,000 or more"], key="ses_total_inc")
    st.selectbox("What is your current living situation?", ["Live alone", "Live with spouse", "Live with another person", "Live with parents", "Live with another Veteran"], key="ses_living")
    st.selectbox("Highest grade level completed, or degree achieved?", ["Less than high school", "High school diploma / GED", "Some college credit", "Bachelor's degree"], key="ses_edu")

# --- SCORING ---
phq_score = sum([{"Not at all":0, "Several days":1, "More than half":2, "Nearly every day":3}[st.session_state[f"p{i}"]] for i in range(9)])
wem_score = sum([{"None":1, "Rarely":2, "Sometimes":3, "Often":4, "Always":5}[st.session_state[f"w{i}"]] for i in range(14)])

if st.button("Generate Full Clinical Report & Service Plan"):
    st.divider()
    
    # --- PART 1: THE CLINICAL REPORT ---
    st.title("📋 Part 1: Clinical Summary Report")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("PHQ-9 (Mood)", phq_score, delta="Urgent" if phq_score >= 15 else None, delta_color="inverse")
    with c2: st.metric("WEMWBS (Well-being)", wem_score, delta="Low" if wem_score < 40 else None, delta_color="inverse")
    with c3: 
        status = "Crisis" if st.session_state.ses_difficulty == "Yes" else "Stable"
        st.metric("Financial Status", status)

    st.subheader("Analysis of Screeners")
    if phq_score >= 10: st.warning(f"Veteran screens positive for Moderate to Severe Depression ({phq_score}).")
    if st.session_state.p8 != "Not at all": st.error("⚠️ CRITICAL: Thoughts of self-harm reported on PHQ-9 Q9.")
    if wem_score < 40: st.info("Well-being score indicates significant lack of mental resilience or optimism.")

    st.divider()

    # --- PART 2: THE TACTICAL SERVICE PLAN ---
    st.title("🛠️ Part 2: Tactical Service Plan")
    
    st.subheader("🏢 SME & Case Management Tasks")
    if st.session_state.ses_difficulty == "Yes":
        st.write("✅ **Basic Needs:** Immediate screening for SSVF or internal Emergency Financial Assistance.")
    if "VA Pension" not in st.session_state.ses_income_src and "Disability related income" not in st.session_state.ses_income_src:
        st.write("✅ **Benefits:** Refer to VSO; Veteran may be eligible for untapped VA disability/pension.")
    if st.session_state.ses_counseling == "No":
        st.write("✅ **Financial:** Mandatory referral to Financial Counseling due to lack of previous exposure.")

    st.subheader("🤝 Peer Support & Outreach")
    if st.session_state.ses_emp_status == "Unemployed":
        st.write(f"✅ **Vocational:** Battle Buddy to assist with resume/job search (Unemployed >{st.session_state.ses_loss_time}).")
    if st.session_state.ses_living == "Live alone":
        st.write("✅ **Social:** Increase wellness check frequency due to isolation risk (Living Alone).")
    if wem_score < 45:
        st.write("✅ **Engagement:** Peer to focus on 'Meaning & Purpose' goal setting.")
