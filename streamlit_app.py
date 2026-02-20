import streamlit as st
import random

st.set_page_config(page_title="SSG Fox Participant Success Tool", layout="wide")

# --- PERSISTENT DATA SYSTEM ---
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
    st.session_state["ses_edu"] = "Some college credit, but less than one year of college credit"

def fill_random():
    for i in range(9): st.session_state[f"p{i}"] = random.choice(["Not at all", "Several days", "More than half", "Nearly every day"])
    for i in range(14): st.session_state[f"w{i}"] = random.choice(["None", "Rarely", "Sometimes", "Often", "Always"])
    for i in range(12): st.session_state[f"i{i}"] = random.choice(["Definitely False", "Probably False", "Probably True", "Definitely True"])
    st.session_state["ses_class"] = random.choice(["Active Duty Member", "Veteran", "Veteran Family Member", "Active Duty Family Member"])
    st.session_state["ses_income_src"] = random.sample(["Disability related income", "VA Pension", "Non-VA Pension", "Retirement benefits (Social Security/ Retirement Savings)", "Employment", "Temporary Financial Assistance", "All Other (family contributions, etc.)"], k=random.randint(1,3))
    st.session_state["ses_emp_status"] = random.choice(["Employed", "Unemployed", "Disabled", "Retired"])
    st.session_state["ses_ft_pt"] = random.choice(["Full-time", "Part-time", "NA"])
    st.session_state["ses_job_loss"] = random.choice(["Yes", "No"])
    st.session_state["ses_loss_time"] = random.choice(["0-6 Months", "6-12 Months", "More than 1 Year", "Not applicable"])
    st.session_state["ses_unemp_ben"] = random.choice(["Yes", "No"])
    st.session_state["ses_unemp_len"] = random.choice(["Less than 6 Weeks", "6-14 Weeks", "15-26 Weeks", "Greater than 26 Weeks", "Not applicable"])
    st.session_state["ses_unemp_amt"] = random.choice(["$0.00-$99.99", "$100.00-$199.99", "$200.00-$299.99", "$300.00-$399.99", "$400.00-$499.99", "Not applicable"])
    st.session_state["ses_tfa"] = random.choice(["Yes", "No", "Pending"])
    st.session_state["ses_counseling"] = random.choice(["Yes", "No", "Pending"])
    st.session_state["ses_difficulty"] = random.choice(["Yes", "No"])
    st.session_state["ses_stress"] = random.choice(["Yes", "No"])
    st.session_state["ses_total_inc"] = random.choice(["Less than $5,000", "$10,000 to $12,499", "$50,000 to $59,999", "$150,000 or more"])
    st.session_state["ses_inc_reduced"] = random.choice(["Yes", "No"])
    st.session_state["ses_reduced_amt"] = random.choice(["Less than $5,000", "$30,000 to $34,999", "Not applicable"])
    st.session_state["ses_living"] = random.choice(["Live alone", "Live with spouse", "Live with another Veteran"])
    st.session_state["ses_area"] = random.choice(["Urban", "Suburban", "Rural"])
    st.session_state["ses_edu"] = random.choice(["Less than high school", "High school diploma / GED", "Bachelor's degree"])

st.title("SSG Fox Participant Success Tool")
st.button("🎲 Randomize All Forms", on_click=fill_random)

tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9", "WEMWBS", "ISEL-12", "SES (Literal PDF Flow)"])

with tab1:
    st.subheader("PHQ-9: Mood Assessment")
    phq_q = ["Little interest or pleasure in doing things", "Feeling down, depressed, or hopeless", "Trouble falling or staying asleep, or sleeping too much", "Feeling tired or having little energy", "Poor appetite or overeating", "Feeling bad about yourself — or that you are a failure or have let yourself or your family down", "Trouble concentrating on things, such as reading the newspaper or watching television", "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual", "Thoughts that you would be better off dead or of hurting yourself in some way"]
    for i, q in enumerate(phq_q):
        st.radio(f"PHQ{i+1}: {q}", ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}")

with tab2:
    st.subheader("WEMWBS: Mental Well-being")
    wem_q = ["I've been feeling optimistic about the future", "I've been feeling useful", "I've been feeling relaxed", "I've been feeling interested in other people", "I've been having energy to spare", "I've been dealing with problems well", "I've been thinking clearly", "I've been feeling good about myself", "I've been feeling close to other people", "I've been feeling confident", "I've been able to make up my own mind about things", "I've been feeling loved", "I've been interested in new things", "I've been feeling cheerful"]
    for i, q in enumerate(wem_q):
        st.radio(f"WEM{i+1}: {q}", ["None", "Rarely", "Sometimes", "Often", "Always"], key=f"w{i}")

with tab3:
    st.subheader("ISEL-12: Social Support Inventory")
    isel_items = ["If I wanted to go on a trip for a day (for example, to the country or mountains), I would have a hard time finding someone to go with me.", "There is no one I can share my most private worries and fears with.", "If I were sick, I could easily find someone to help me with my daily chores.", "There is someone I can turn to for advice about making very important decisions or for help with family problems.", "I could easily find someone who would like to go to a movie with me.", "When I need suggestions on how to deal with a personal problem, I know someone I can turn to.", "I don't often get invited to do things with others.", "If I had to go out of town for a few weeks, it would be difficult to find someone who would look after my house or apartment (the plants, pets, garden, etc.).", "If I wanted to have lunch with someone, I could easily find someone to join me.", "If I was stranded 10 miles from home, there is someone I could call who could come and get me.", "If a crisis arose in my life, I would have a hard time finding someone who could give me good advice.", "If I were moving, I would have a hard time finding someone to help me."]
    for i, q in enumerate(isel_items):
        st.selectbox(q, ["Definitely False", "Probably False", "Probably True", "Definitely True"], key=f"i{i}")

with tab4:
    st.header("Socio-Economic Status (Literal Map)")
    st.selectbox("Select Individual Classification:", ["Active Duty Member", "Veteran", "Veteran Family Member", "Active Duty Family Member"], key="ses_class")
    st.multiselect("What are your regular sources of income? [SELECT ALL THAT APPLY]", ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement benefits (Social Security/ Retirement Savings)", "Employment", "Temporary Financial Assistance", "All Other (family contributions, etc.)"], key="ses_income_src")
    st.selectbox("What is your current employment status? [SELECT ONE]", ["Employed", "Unemployed", "Disabled", "Retired"], key="ses_emp_status")
    st.selectbox("Is it full-time or part-time? [SELECT ONE]", ["Full-time", "Part-time", "NA"], key="ses_ft_pt")
    st.radio("Did you lose your job? [SELECT ONE]", ["Yes", "No"], key="ses_job_loss")
    st.selectbox("Approximately how long ago did you lose your job? [SELECT ONE]", ["0-6 Months", "6-12 Months", "More than 1 Year", "Not applicable"], key="ses_loss_time")
    st.radio("Are you receiving unemployment benefits? [SELECT ONE]", ["Yes", "No"], key="ses_unemp_ben")
    st.selectbox("If yes, how long have you been receiving unemployment benefits? [SELECT ONE]", ["Less than 6 Weeks", "6-14 Weeks", "15-26 Weeks", "Greater than 26 Weeks", "Not applicable"], key="ses_unemp_len")
    st.selectbox("How much are your weekly unemployment benefits? [SELECT ONE]", ["$0.00-$99.99", "$100.00-$199.99", "$200.00-$299.99", "$300.00-$399.99", "$400.00-$499.99", "Not applicable"], key="ses_unemp_amt")
    st.radio("Are you receiving any temporary financial assistance? [SELECT ONE]", ["Yes", "No", "Pending"], key="ses_tfa")
    st.radio("Have you ever received financial counseling services? [SELECT ONE]", ["Yes", "No", "Pending"], key="ses_counseling")
    st.radio("Have you had difficulty covering medical, food, and housing expenses? [SELECT ONE]", ["Yes", "No"], key="ses_difficulty")
    st.radio("Are you experiencing any stress over your financial situation? [SELECT ONE]", ["Yes", "No"], key="ses_stress")
    st.selectbox("Total Household Income (Last 12 months) [SELECT ONE]", ["Less than $5,000", "$5,000 to $7,499", "$10,000 to $12,499", "$25,000 to $29,999", "$50,000 to $59,999", "$150,000 or more"], key="ses_total_inc")
    st.radio("Has your income been reduced? [SELECT ONE]", ["Yes", "No"], key="ses_inc_reduced")
    st.selectbox("How much has your income been reduced? (annual estimate) [SELECT ONE]", ["Less than $5,000", "$15,000 to $19,999", "$30,000 to $34,999", "Not applicable"], key="ses_reduced_amt")
    st.selectbox("What is your current living situation? [SELECT ONE]", ["Live alone", "Live with spouse", "Live with another person", "Live with parents", "Live with another Veteran"], key="ses_living")
    st.selectbox("Which of the following best describes the area you live in? [SELECT ONE]", ["Urban", "Suburban", "Rural"], key="ses_area")
    st.selectbox("Highest grade level completed, or degree achieved? [SELECT ONE]", ["Less than high school", "High school diploma / GED", "Some college credit, but less than one year of college credit", "Bachelor's degree"], key="ses_edu")

# --- CALCULATION LOGIC ---
phq_score = sum([{"Not at all":0, "Several days":1, "More than half":2, "Nearly every day":3}[st.session_state[f"p{i}"]] for i in range(9)])
wem_score = sum([{"None":1, "Rarely":2, "Sometimes":3, "Often":4, "Always":5}[st.session_state[f"w{i}"]] for i in range(14)])
isel_score = sum([{"Definitely False":0, "Probably False":1, "Probably True":2, "Definitely True":3}[st.session_state[f"i{i}"]] for i in range(12)])

# --- NEW EXPANDED REPORT ---
if st.button("Generate Comprehensive Service Plan"):
    st.divider()
    
    # HEADER SECTION
    st.title("📋 SSG Fox Tactical Service Plan")
    st.info(f"Summary Metrics: PHQ-9: {phq_score} (Mood) | WEMWBS: {wem_score} (Well-being) | ISEL-12: {isel_score} (Support)")

    # 1. CRISIS & URGENT TRIAGE
    st.subheader("🚨 1. Urgent Triage")
    colA, colB = st.columns(2)
    with colA:
        if st.session_state.p8 != "Not at all":
            st.error("Suicide Ideation Flagged (PHQ-9 Q9). Immediate clinical warm hand-off required.")
        if st.session_state.ses_difficulty == "Yes":
            st.error("Basic Needs Crisis: Difficulty covering Food, Medical, or Housing.")
    with colB:
        if phq_score >= 15:
            st.warning(f"High PHQ-9 Score ({phq_score}): Severe depressive symptoms.")
        if st.session_state.ses_stress == "Yes":
            st.warning("High Financial Stress: Subjective experience of financial distress.")

    # 2. CASE MANAGEMENT (SME) ACTIONS
    st.subheader("🏢 2. Case Management (SME Tasks)")
    cm_tasks = []
    if st.session_state.ses_counseling == "No":
        cm_tasks.append("Refer to internal or partner Financial Counseling (Never received).")
    if not any(x in st.session_state.ses_income_src for x in ["VA Pension", "Disability related income"]):
        cm_tasks.append("Incomplete VA Benefits: Referral to VSO for disability/pension claim review.")
    if st.session_state.ses_unemp_ben == "No" and st.session_state.ses_emp_status == "Unemployed":
        cm_tasks.append("Unemployment Insurance: Assist Veteran in applying for state/federal benefits.")
    if st.session_state.ses_tfa == "No" and st.session_state.ses_difficulty == "Yes":
        cm_tasks.append("TFA Assessment: Evaluate eligibility for SSVF or internal Temporary Financial Assistance.")
    
    if cm_tasks:
        for t in cm_tasks: st.write(f"✅ {t}")
    else:
        st.write("No specific SME tasks flagged.")

    # 3. PEER SUPPORT (BATTLE BUDDY) ACTIONS
    st.subheader("🤝 3. Peer Support (Battle Buddy Tasks)")
    peer_tasks = []
    if st.session_state.ses_emp_status == "Unemployed":
        peer_tasks.append(f"Vocational Support: Peer to accompany to job fairs (Unemployed for {st.session_state.ses_loss_time}).")
    if isel_score < 18:
        peer_tasks.append("Social Integration: Introduce to Veteran service organizations or coffee socials (Low social support).")
    if wem_score < 40:
        peer_tasks.append("Meaning & Purpose: Weekly 1:1 check-ins focused on small 'wins' and future optimism.")
    if st.session_state.ses_living == "Live alone":
        peer_tasks.append("Isolation Check: Increase frequency of check-ins for Veteran living alone.")

    if peer_tasks:
        for t in peer_tasks: st.write(f"✅ {t}")
    else:
        st.write("No specific Peer tasks flagged.")

    st.divider()
    st.caption("This report is a decision-support tool. Final clinical judgment rests with the SSG Fox Staff.")
