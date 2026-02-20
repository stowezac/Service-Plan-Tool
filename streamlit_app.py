import streamlit as st
import random

st.set_page_config(page_title="SSG Fox Heavy-Duty Tool", layout="wide")

# --- PERSISTENT DATA SYSTEM ---
if 'init' not in st.session_state:
    st.session_state.init = True
    for i in range(9): st.session_state[f"p{i}"] = "Not at all"
    for i in range(14): st.session_state[f"w{i}"] = "Sometimes"
    for i in range(12): st.session_state[f"i{i}"] = "Probably True"
    # SES Defaults
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
    st.session_state["er_visits"] = random.choice(["0", "1", "2", "3+"])
    st.session_state["legal_issues"] = random.choice(["No", "Yes"])
    st.session_state["income_src"] = random.sample(["Disability related income", "VA Pension", "Non-VA Pension", "Employment", "Social Security", "TFA"], k=random.randint(1,3))

st.title("SSG Fox Participant Success Tool")
st.button("🎲 Randomize All Forms", on_click=fill_random)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9 (Mood)", "WEMWBS (Well-being)", "ISEL-12 (Social)", "Full SES (Economic)"])

# --- TAB 1: PHQ-9 ---
with tab1:
    phq_q = ["Little interest or pleasure", "Feeling down, depressed, hopeless", "Trouble sleeping", "Feeling tired/little energy", "Poor appetite/overeating", "Feeling like a failure", "Trouble concentrating", "Moving slowly/Fidgety", "Thoughts of self-harm"]
    phq_ans = [st.radio(f"PHQ{i+1}: {q}", ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}") for i, q in enumerate(phq_q)]
    phq_score = sum([{"Not at all":0, "Several days":1, "More than half":2, "Nearly every day":3}[a] for a in phq_ans])

# --- TAB 2: WEMWBS ---
with tab2:
    wem_q = ["Optimistic", "Useful", "Relaxed", "Interested in people", "Energy", "Problem solving", "Thinking clearly", "Self-worth", "Closeness", "Confidence", "Loved", "Decision making", "New things", "Cheerful"]
    wem_ans = [st.radio(f"WEM{i+1}: {q}", ["None", "Rarely", "Sometimes", "Often", "Always"], key=f"w{i}") for i, q in enumerate(wem_q)]
    wem_score = sum([{"None":1, "Rarely":2, "Sometimes":3, "Often":4, "Always":5}[a] for a in wem_ans])

# --- TAB 3: ISEL-12 ---
with tab3:
    isel_items = [
        ("I’d have a hard time finding someone to go on a trip with me.", "Tangible", True),
        ("There is no one I can share my most private worries with.", "Appraisal", True),
        ("If I were sick, I could easily find help with chores.", "Tangible", False),
        ("I have someone to turn to for advice about family problems.", "Appraisal", False),
        ("I could easily find someone to go to a movie with.", "Belonging", False),
        ("When I need suggestions for a personal problem, I have someone to turn to.", "Appraisal", False),
        ("I don’t often get invited to do things with others.", "Belonging", True),
        ("If I went out of town, someone would look after my house.", "Tangible", False),
        ("If I wanted lunch, I could easily find someone to join me.", "Belonging", False),
        ("If I was stranded, someone would come and get me.", "Tangible", False),
        ("If a crisis arose, it would be hard to find advice.", "Appraisal", True),
        ("If I needed help moving, I’d have a hard time finding help.", "Tangible", True)
    ]
    cat_scores = {"Tangible": 0, "Appraisal": 0, "Belonging": 0}
    for i, (q, cat, is_reverse) in enumerate(isel_items):
        a = st.selectbox(q, ["Definitely False", "Probably False", "Probably True", "Definitely True"], key=f"i{i}")
        val = {"Definitely False":1, "Probably False":2, "Probably True":3, "Definitely True":4}[a]
        if is_reverse: val = 5 - val
        cat_scores[cat] += val

# --- TAB 4: MAPPED SES ---
with tab4:
    st.header("Socio-Economic Status (SES)")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Demographics & Housing")
        st.selectbox("Marital Status", ["Single", "Married", "Separated", "Divorced", "Widowed"], key="marital")
        st.selectbox("Current Living Situation", ["Renting", "Own Home", "Staying with friends/family", "Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge", "VASH", "GPD", "Other"], key="living")
        st.radio("Are you currently experiencing legal issues (parole, warrants, court)?", ["No", "Yes"], key="legal_issues")
        
        st.subheader("Health & Wellness")
        st.select_slider("Overall Health Rating", ["Poor", "Fair", "Good", "Excellent"], key="health_rating")
        st.selectbox("How many ER visits in the last 6 months?", ["0", "1", "2", "3", "4+"], key="er_visits")
        
    with col2:
        st.subheader("Financial & Employment")
        st.selectbox("Employment Status", ["Employed Full-Time", "Employed Part-Time", "Unemployed", "Disabled", "Retired"], key="emp_status")
        st.radio("If unemployed, are you actively looking for work?", ["No", "Yes"], key="looking_work")
        st.multiselect("Sources of Income", ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement", "Employment", "Social Security", "Public Assistance", "TFA (Temp Financial Assistance)", "No Income"], key="income_src")
        st.radio("Difficulty covering basic needs (Food/Housing/Medical)?", ["No", "Yes"], key="needs")
        st.radio("Has your income been reduced by $30k+ recently?", ["No", "Yes"], key="income_drop")
        st.slider("Overall Financial Stress (1-10)", 1, 10, key="stress")
