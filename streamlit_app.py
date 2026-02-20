import streamlit as st
import random

st.set_page_config(page_title="SSG Fox Participant Tool", layout="wide")

# --- PERSISTENT DATA SYSTEM ---
if 'init' not in st.session_state:
    st.session_state.init = True
    for i in range(9): st.session_state[f"p{i}"] = "Not at all"
    for i in range(14): st.session_state[f"w{i}"] = "Sometimes"
    for i in range(12): st.session_state[f"i{i}"] = "Probably True"
    st.session_state["marital"] = "Single"
    st.session_state["living"] = "Renting"
    st.session_state["emp_status"] = "Employed Full-Time"
    st.session_state["looking_work"] = "No"
    st.session_state["income_src"] = []
    st.session_state["needs"] = "No"
    st.session_state["income_drop"] = "No"
    st.session_state["stress"] = 5
    st.session_state["health_rating"] = "Good"
    st.session_state["er_visits"] = "0"
    st.session_state["legal_issues"] = "No"

def fill_random():
    for i in range(9): st.session_state[f"p{i}"] = random.choice(["Not at all", "Several days", "More than half", "Nearly every day"])
    for i in range(14): st.session_state[f"w{i}"] = random.choice(["None", "Rarely", "Sometimes", "Often", "Always"])
    for i in range(12): st.session_state[f"i{i}"] = random.choice(["Definitely False", "Probably False", "Probably True", "Definitely True"])
    st.session_state["marital"] = random.choice(["Single", "Married", "Separated", "Divorced", "Widowed"])
    st.session_state["living"] = random.choice(["Renting", "Own Home", "Staying with friends/family", "Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge", "VASH", "GPD"])
    st.session_state["emp_status"] = random.choice(["Employed Full-Time", "Employed Part-Time", "Unemployed", "Disabled", "Retired"])
    st.session_state["looking_work"] = random.choice(["No", "Yes"])
    st.session_state["needs"] = random.choice(["No", "Yes"])
    st.session_state["income_drop"] = random.choice(["No", "Yes"])
    st.session_state["stress"] = random.randint(1, 10)
    st.session_state["health_rating"] = random.choice(["Poor", "Fair", "Good", "Excellent"])
    st.session_state["er_visits"] = random.choice(["0", "1", "2", "3", "4+"])
    st.session_state["legal_issues"] = random.choice(["No", "Yes"])
    st.session_state["income_src"] = random.sample(["Disability related income", "VA Pension", "Non-VA Pension", "Employment", "Social Security", "TFA"], k=random.randint(1,3))

st.title("SSG Fox Participant Success Tool")
st.button("🎲 Randomize All Forms", on_click=fill_random)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9", "WEMWBS", "ISEL-12", "Full SES"])

# --- TAB 1: PHQ-9 ---
with tab1:
    phq_q = ["Little interest or pleasure", "Feeling down, depressed, hopeless", "Trouble sleeping", "Feeling tired/little energy", "Poor appetite/overeating", "Feeling like a failure", "Trouble concentrating", "Moving slowly/Fidgety", "Thoughts of self-harm"]
    for i, q in enumerate(phq_q):
        st.radio(f"PHQ{i+1}: {q}", ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}")

# --- TAB 2: WEMWBS ---
with tab2:
    wem_q = ["Optimistic", "Useful", "Relaxed", "Interested in people", "Energy", "Problem solving", "Thinking clearly", "Self-worth", "Closeness", "Confidence", "Loved", "Decision making", "New things", "Cheerful"]
    for i, q in enumerate(wem_q):
        st.radio(f"WEM{i+1}: {q}", ["None", "Rarely", "Sometimes", "Often", "Always"], key=f"w{i}")

# --- TAB 3: ISEL-12 ---
with tab3:
    st.write("Social Support Inventory")
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

# --- TAB 4: SES (REVERTED TO PAPERWORK STYLE) ---
with tab4:
    st.header("Socio-Economic Status")
    st.selectbox("Marital Status", ["Single", "Married", "Separated", "Divorced", "Widowed"], key="marital")
    st.selectbox("Current Living Situation", ["Renting", "Own Home", "Staying with friends/family", "Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge", "VASH", "GPD", "Other"], key="living")
    st.radio("Are you currently experiencing legal issues (parole, warrants, court)?", ["No", "Yes"], key="legal_issues")
    st.select_slider("Overall Health Rating", ["Poor", "Fair", "Good", "Excellent"], key="health_rating")
    st.selectbox("How many ER visits in the last 6 months?", ["0", "1", "2", "3", "4+"], key="er_visits")
    st.selectbox("Employment Status", ["Employed Full-Time", "Employed Part-Time", "Unemployed", "Disabled", "Retired"], key="emp_status")
    st.radio("If unemployed, are you actively looking for work?", ["No", "Yes"], key="looking_work")
    st.multiselect("Sources of Income", ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement", "Employment", "Social Security", "Public Assistance", "TFA (Temp Financial Assistance)", "No Income"], key="income_src")
    st.radio("Difficulty covering basic needs (Food/Housing/Medical)?", ["No", "Yes"], key="needs")
    st.radio("Has your income been reduced by $30k+ recently?", ["No", "Yes"], key="income_drop")
    st.slider("Overall Financial Stress (1-10)", 1, 10, key="stress")

# --- LOGIC CALCS FOR REPORT ---
phq_score = sum([{"Not at all":0, "Several days":1, "More than half":2, "Nearly every day":3}[st.session_state[f"p{i}"]] for i in range(9)])
wem_score = sum([{"None":1, "Rarely":2, "Sometimes":3, "Often":4, "Always":5}[st.session_state[f"w{i}"]] for i in range(14)])

# --- REPORT GENERATOR ---
if st.button("Generate Service Plan Report"):
    st.divider()
    
    # SECTION 1: THE STRUGGLE PROFILE
    st.title("📋 Part 1: Struggle Profile")
    colA, colB = st.columns(2)
    
    with colA:
        st.subheader("🔴 Urgent Risks")
        if st.session_state.p8 != "Not at all": st.error("Suicide Ideation Flagged")
        if st.session_state.living in ["Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"]: st.error(f"Housing Crisis: {st.session_state.living}")
        if st.session_state.needs == "Yes": st.error("Basic Needs Deficiency")
        if st.session_state.legal_issues == "Yes": st.error("Active Legal Barriers")

    with colB:
        st.subheader("🟡 Functional Barriers")
        if phq_score >= 10: st.warning(f"Depression Symptoms: {phq_score}")
        if st.session_state.emp_status == "Unemployed": st.warning("Vocational Instability")
        if st.session_state.health_rating == "Poor": st.warning("Health Instability")

    st.divider()

    # SECTION 2: TACTICAL SERVICE PLAN
    st.title("🛠️ Part 2: Tactical Service Plan")
    
    st.subheader("🏢 Case Management (SME Tasks)")
    if st.session_state.living in ["Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"]:
        st.write("- **Housing:** Referral to SSVF/HUD-VASH for stable placement.")
    if not any(x in st.session_state.income_src for x in ["VA Pension", "Disability related income"]):
        st.write("- **Benefits:** Connect with VSO for Claims review.")
    if phq_score >= 15:
        st.write("- **Clinical:** Facilitate hand-off to VA Mental Health.")

    st.subheader("🤝 Peer Support (Battle Buddy Tasks)")
    if st.session_state.looking_work == "Yes":
        st.write("- **Vocational:** Peer to accompany to job fairs/workforce center.")
    if wem_score < 40:
        st.write("- **Engagement:** Weekly Peer check-ins focused on 'Small Wins'.")
    if st.session_state.stress >= 7:
        st.write("- **Logistics:** Peer to assist with organizing mail/financial paperwork.")

    st.divider()
    st.write(f"**Final Metrics for Grant Tracking:** PHQ: {phq_score}, WEM: {wem_score}, Stress: {st.session_state.stress}/10")
