import streamlit as st
import random

st.set_page_config(page_title="SSG Fox Heavy-Duty Tool", layout="wide")

# --- PERSISTENT DATA SYSTEM ---
if 'init' not in st.session_state:
    st.session_state.init = True
    for i in range(9): st.session_state[f"p{i}"] = "Not at all"
    for i in range(14): st.session_state[f"w{i}"] = "Sometimes"
    for i in range(12): st.session_state[f"i{i}"] = "Probably True"
    st.session_state["marital"] = "Single"
    st.session_state["living"] = "Renting"
    st.session_state["emp_status"] = "Employed Full-Time"
    st.session_state["income_src"] = []
    st.session_state["needs"] = "No"
    st.session_state["income_drop"] = "No"
    st.session_state["stress"] = 5

def fill_random():
    for i in range(9): st.session_state[f"p{i}"] = random.choice(["Not at all", "Several days", "More than half", "Nearly every day"])
    for i in range(14): st.session_state[f"w{i}"] = random.choice(["None", "Rarely", "Sometimes", "Often", "Always"])
    for i in range(12): st.session_state[f"i{i}"] = random.choice(["Definitely False", "Probably False", "Probably True", "Definitely True"])
    st.session_state["marital"] = random.choice(["Single", "Married", "Separated", "Divorced", "Widowed"])
    st.session_state["living"] = random.choice(["Renting", "Own Home", "Staying with friends/family", "Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"])
    st.session_state["emp_status"] = random.choice(["Employed Full-Time", "Employed Part-Time", "Unemployed", "Disabled", "Retired", "Student"])
    st.session_state["needs"] = random.choice(["No", "Yes"])
    st.session_state["income_drop"] = random.choice(["No", "Yes"])
    st.session_state["stress"] = random.randint(1, 10)
    st.session_state["income_src"] = random.sample(["Disability related income", "VA Pension", "Non-VA Pension", "Employment", "Social Security"], k=random.randint(1,3))

st.title("SSG Fox Participant Success Tool")
st.button("🎲 Randomize All Forms", on_click=fill_random)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9 (Mood)", "WEMWBS (Well-being)", "ISEL-12 (Social)", "Full SES (Economic)"])

# --- TAB 1: PHQ-9 ---
with tab1:
    phq_q = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself or that you are a failure",
        "Trouble concentrating on things",
        "Moving or speaking so slowly or being fidgety/restless",
        "Thoughts that you would be better off dead or of hurting yourself"
    ]
    phq_ans = [st.radio(f"PHQ{i+1}: {q}", ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}") for i, q in enumerate(phq_q)]
    phq_score = sum([{"Not at all":0, "Several days":1, "More than half":2, "Nearly every day":3}[a] for a in phq_ans])

# --- TAB 2: WEMWBS ---
with tab2:
    wem_q = [
        "Optimistic about the future", "Feeling useful", "Feeling relaxed", "Interested in other people",
        "Energy to spare", "Dealing with problems well", "Thinking clearly", "Feeling good about myself",
        "Feeling close to other people", "Feeling confident", "Feeling loved", "Able to make up my own mind",
        "Interested in new things", "Feeling cheerful"
    ]
    wem_ans = [st.radio(f"WEM{i+1}: {q}", ["None", "Rarely", "Sometimes", "Often", "Always"], key=f"w{i}") for i, q in enumerate(wem_q)]
    wem_score = sum([{"None":1, "Rarely":2, "Sometimes":3, "Often":4, "Always":5}[a] for a in wem_ans])

# --- TAB 3: ISEL-12 ---
with tab3:
    st.write("ISEL-12 Social Support Score (Sub-scales calculated automatically)")
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
        if is_reverse:
            val = 5 - val
        cat_scores[cat] += val

# --- TAB 4: SES ---
with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Marital Status", ["Single", "Married", "Separated", "Divorced", "Widowed"], key="marital")
        st.selectbox("Living Situation", ["Renting", "Own Home", "Staying with friends/family", "Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"], key="living")
        st.selectbox("Employment Status", ["Employed Full-Time", "Employed Part-Time", "Unemployed", "Disabled", "Retired", "Student"], key="emp_status")
    with col2:
        st.multiselect("Sources of Income", ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement", "Employment", "Social Security", "Public Assistance", "No Income"], key="income_src")
        st.radio("Difficulty covering basic needs (Food/Housing)?", ["No", "Yes"], key="needs")
        st.radio("Income reduced by $30k+ recently?", ["No", "Yes"], key="income_drop")
    st.slider("Financial Stress Level", 1, 10, key="stress")

# --- REPORT GENERATION ---
if st.button("Generate Comprehensive 2-Part Report"):
    st.divider()
    
    # PART 1: STRUGGLE PROFILE
    st.title("📋 Part 1: Participant Struggle Profile")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.subheader("🔴 Immediate Risks")
        if st.session_state.p8 != "Not at all": st.error("Suicide Ideation Flagged (PHQ-9 Q9)")
        if st.session_state.living in ["Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"]: st.error(f"Unstable Housing: {st.session_state.living}")
        if st.session_state.needs == "Yes": st.error("Basic Needs Deficiency")
        
    with c2:
        st.subheader("🟡 Functional Barriers")
        if phq_score >= 10: st.warning(f"Moderate/Severe Depression ({phq_score})")
        if st.session_state.emp_status == "Unemployed": st.warning("Vocational Instability")
        if cat_scores['Tangible'] <= 10: st.warning("Critical Lack of Physical Support")
        
    with c3:
        st.subheader("🔵 Growth & Wellness")
        if wem_score < 40: st.info(f"Low Mental Well-being ({wem_score})")
        if cat_scores['Appraisal'] <= 10: st.info("Lack of Confidant/Advice")
        if cat_scores['Belonging'] <= 10: st.info("High Social Isolation")

    st.divider()

    # PART 2: TACTICAL SERVICE PLAN
    st.title("🛠️ Part 2: Tactical Service Plan")
    
    # CASE MANAGEMENT
    st.header("🏢 Case Management (SME Focus)")
    with st.expander("View Systemic & Resource Actions", expanded=True):
        if st.session_state.living in ["Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"]:
            st.write("👉 **HOUSING:** Immediate SSVF/HUD-VASH referral. Assist with gathering ID/DD214 docs.")
        if not any(x in st.session_state.income_src for x in ["VA Pension", "Disability related income"]):
            st.write("👉 **BENEFITS:** Connect with VSO. Check PACT Act eligibility for chronic conditions.")
        if phq_score >= 15:
            st.write("👉 **CLINICAL:** Warm hand-off to VA Mental Health or community clinical partner.")
        if st.session_state.emp_status == "Unemployed":
            st.write("👉 **VOCATIONAL:** Refer to DVOP or local workforce development rep.")

    # PEER SUPPORT
    st.header("🤝 Peer Support (Battle Buddy Focus)")
    with st.expander("View Relational & Logistical Actions", expanded=True):
        if cat_scores['Tangible'] <= 10:
            st.write("👉 **LOGISTICS:** Peer to provide direct transport to next 3 medical/VSO appointments.")
        if st.session_state.w1 in ["None", "Rarely"]: # Feeling Useful
            st.write("👉 **PURPOSE:** Identify one task where Veteran can 'give back' (mentorship, volunteering).")
        if cat_scores['Belonging'] <= 10:
            st.write("👉 **CONNECTION:** Peer to attend a 'no-pressure' Veteran social (coffee/breakfast) with Participant.")
        if cat_scores['Appraisal'] <= 10:
            st.write("👉 **TRUST:** Establish weekly 10-minute relational check-ins (phone or coffee).")
        if st.session_state.stress >= 7:
            st.write("👉 **DE-STRESS:** Peer to help sort bills/mail into priority categories to reduce overwhelm.")

    st.divider()
    st.subheader("Grant Metric Baseline")
    st.write(f"**PHQ-9:** {phq_score} | **WEMWBS:** {wem_score} | **Social (ISEL Total):** {sum(cat_scores.values())}")
