import streamlit as st
import random

st.set_page_config(page_title="SSG Fox Participant Success Tool", layout="wide")

# --- INITIALIZATION ---
if 'init' not in st.session_state:
    st.session_state.init = True
    # Standard SSG Fox Screeners
    for i in range(9): st.session_state[f"p{i}"] = "Not at all"
    for i in range(14): st.session_state[f"w{i}"] = "Sometimes"
    for i in range(12): st.session_state[f"i{i}"] = "Probably True"
    # SES LITERAL FIELDS
    st.session_state["ses_marital"] = "Single"
    st.session_state["ses_living"] = "Renting"
    st.session_state["ses_living_other"] = ""
    st.session_state["ses_legal"] = "No"
    st.session_state["ses_health"] = "Good"
    st.session_state["ses_er"] = "0"
    st.session_state["ses_employment"] = "Employed Full-Time"
    st.session_state["ses_looking"] = "No"
    st.session_state["ses_income_sources"] = []
    st.session_state["ses_basic_needs"] = "No"
    st.session_state["ses_income_drop"] = "No"
    st.session_state["ses_financial_stress"] = 5

def fill_random():
    for i in range(9): st.session_state[f"p{i}"] = random.choice(["Not at all", "Several days", "More than half", "Nearly every day"])
    for i in range(14): st.session_state[f"w{i}"] = random.choice(["None", "Rarely", "Sometimes", "Often", "Always"])
    for i in range(12): st.session_state[f"i{i}"] = random.choice(["Definitely False", "Probably False", "Probably True", "Definitely True"])
    st.session_state["ses_marital"] = random.choice(["Single", "Married", "Separated", "Divorced", "Widowed", "Partnered"])
    st.session_state["ses_living"] = random.choice(["Renting", "Own Home", "Staying with friends/family", "Motel/Hotel", "Homeless Shelter", "VASH", "GPD", "Outdoors/Car"])
    st.session_state["ses_legal"] = random.choice(["No", "Yes"])
    st.session_state["ses_health"] = random.choice(["Poor", "Fair", "Good", "Excellent"])
    st.session_state["ses_er"] = random.choice(["0", "1", "2", "3", "4+"])
    st.session_state["ses_employment"] = random.choice(["Employed Full-Time", "Employed Part-Time", "Unemployed", "Disabled", "Retired"])
    st.session_state["ses_looking"] = random.choice(["No", "Yes"])
    st.session_state["ses_income_sources"] = random.sample(["VA Pension", "VA Disability", "Employment", "Social Security", "Public Assistance", "TFA", "No Income"], k=2)
    st.session_state["ses_basic_needs"] = random.choice(["No", "Yes"])
    st.session_state["ses_income_drop"] = random.choice(["No", "Yes"])
    st.session_state["ses_financial_stress"] = random.randint(1, 10)

st.title("SSG Fox Participant Success Tool")
st.button("🎲 Randomize All Forms", on_click=fill_random)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9", "WEMWBS", "ISEL-12", "Socio-Economic Status (SES)"])

with tab1:
    phq_q = ["Little interest or pleasure", "Feeling down, depressed, hopeless", "Trouble sleeping", "Feeling tired/little energy", "Poor appetite/overeating", "Feeling like a failure", "Trouble concentrating", "Moving slowly/Fidgety", "Thoughts of self-harm"]
    for i, q in enumerate(phq_q):
        st.radio(f"PHQ{i+1}: {q}", ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}")

with tab2:
    wem_q = ["Optimistic", "Useful", "Relaxed", "Interested in people", "Energy", "Problem solving", "Thinking clearly", "Self-worth", "Closeness", "Confidence", "Loved", "Decision making", "New things", "Cheerful"]
    for i, q in enumerate(wem_q):
        st.radio(f"WEM{i+1}: {q}", ["None", "Rarely", "Sometimes", "Often", "Always"], key=f"w{i}")

with tab3:
    st.write("Social Support Inventory (ISEL-12)")
    isel_items = [
        "I’d have a hard time finding someone to go on a trip with me.",
        "There is no one I can share my most private worries with.",
        "If I were sick, I could easily find help with chores.",
        "I have someone to turn to for advice about family problems.",
        "I could easily find someone to go to a movie with.",
        "When I need suggestions for a personal problem, I have someone to turn to.",
        "I don’t often get invited to do things with others.",
        "If I went out of town, someone would look after my house.",
        "If I wanted lunch, I could easily find someone to join me.",
        "If I was stranded, someone would come and get me.",
        "If a crisis arose, it would be hard to find advice.",
        "If I needed help moving, I’d have a hard time finding help."
    ]
    for i, q in enumerate(isel_items):
        st.selectbox(q, ["Definitely False", "Probably False", "Probably True", "Definitely True"], key=f"i{i}")

with tab4:
    st.header("Baseline Socio-Economic Status")
    
    st.selectbox("Marital Status", ["Single", "Married", "Separated", "Divorced", "Widowed", "Partnered", "Other"], key="ses_marital")
    
    st.selectbox("Current Living Situation", ["Renting", "Own Home", "Staying with friends/family", "Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge", "VASH", "GPD", "Other"], key="ses_living")
    if st.session_state.ses_living == "Other":
        st.text_input("If Other, please specify:", key="ses_living_other")
    
    st.radio("Are you currently experiencing legal issues (parole, warrants, court, etc.)?", ["No", "Yes"], key="ses_legal")
    
    st.select_slider("Overall Health Rating", ["Poor", "Fair", "Good", "Excellent"], key="ses_health")
    
    st.selectbox("How many ER visits in the last 6 months?", ["0", "1", "2", "3", "4+"], key="ses_er")
    
    st.selectbox("Employment Status", ["Employed Full-Time", "Employed Part-Time", "Unemployed", "Disabled", "Retired", "Student", "Other"], key="ses_employment")
    
    st.radio("If unemployed, are you actively looking for work?", ["No", "Yes", "N/A"], key="ses_looking")
    
    st.multiselect("Regular sources of income (Select all that apply)", ["Employment", "VA Disability", "VA Pension", "Non-VA Pension", "Social Security", "Public Assistance", "TFA", "No Income", "Other"], key="ses_income_sources")
    
    st.radio("Are you having difficulty covering basic needs (Food, Medical, Housing)?", ["No", "Yes"], key="ses_basic_needs")
    
    st.radio("Has your annual income been reduced by $30,000 or more in the past 12 months?", ["No", "Yes"], key="ses_income_drop")
    
    st.slider("Financial Stress Level (1 = None, 10 = Extreme)", 1, 10, key="ses_financial_stress")

# --- DATA PROCESSING ---
phq_score = sum([{"Not at all":0, "Several days":1, "More than half":2, "Nearly every day":3}[st.session_state[f"p{i}"]] for i in range(9)])
wem_score = sum([{"None":1, "Rarely":2, "Sometimes":3, "Often":4, "Always":5}[st.session_state[f"w{i}"]] for i in range(14)])

# --- REPORT GENERATION ---
if st.button("Generate Tactical Service Plan"):
    st.divider()
    
    st.title("📋 Part 1: Struggle Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔴 Urgent Risks")
        if st.session_state.p8 != "Not at all": st.error("⚠️ Suicide Ideation Flagged (PHQ-9 Q9)")
        if st.session_state.ses_living in ["Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"]: st.error(f"⚠️ Housing Crisis: {st.session_state.ses_living}")
        if st.session_state.ses_basic_needs == "Yes": st.error("⚠️ Basic Needs Deficiency")
        if st.session_state.ses_legal == "Yes": st.error("⚠️ Active Legal Barriers")

    with col2:
        st.subheader("🟡 Functional Barriers")
        if phq_score >= 10: st.warning(f"Depression Symptoms: {phq_score}")
        if st.session_state.ses_employment == "Unemployed": st.warning("Vocational Instability")
        if st.session_state.ses_health == "Poor": st.warning("Health Instability")
        if int(st.session_state.ses_er.replace('4+', '4')) >= 2: st.warning("Frequent ER Utilization")

    st.divider()

    st.title("🛠️ Part 2: Tactical Service Plan")
    
    # CASE MANAGEMENT TASKS
    st.subheader("🏢 Case Management (SME Tasks)")
    if st.session_state.ses_living in ["Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"]:
        st.write("- **Housing:** Immediate SSVF/HUD-VASH referral.")
    if "VA Pension" not in st.session_state.ses_income_sources and "VA Disability" not in st.session_state.ses_income_sources:
        st.write("- **Benefits:** Connect with VSO (Veteran is not receiving VA-specific income).")
    if phq_score >= 15:
        st.write("- **Clinical:** Facilitate hand-off to VA Mental Health.")

    # PEER SUPPORT TASKS
    st.subheader("🤝 Peer Support (Battle Buddy Tasks)")
    if st.session_state.ses_looking == "Yes":
        st.write("- **Vocational:** Peer to accompany to job fairs or workforce center.")
    if wem_score < 40:
        st.write("- **Engagement:** Weekly check-ins focused on community connection.")
    if st.session_state.ses_financial_stress >= 7:
        st.write("- **Stress Reduction:** Peer to assist with organizing mail and financial triage.")

    st.divider()
    st.write(f"**Baseline Metrics:** PHQ: {phq_score} | WEM: {wem_score} | Stress: {st.session_state.ses_financial_stress}/10")
