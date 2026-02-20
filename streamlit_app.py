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

# --- DATA ENTRY ---
with tab1:
    phq_q = ["Little interest or pleasure in doing things", "Feeling down, depressed, or hopeless", "Trouble falling or staying asleep, or sleeping too much", "Feeling tired or having little energy", "Poor appetite or overeating", "Feeling bad about yourself — or that you are a failure", "Trouble concentrating on things", "Moving or speaking so slowly... or being fidgety/restless", "Thoughts that you would be better off dead or of hurting yourself"]
    phq_answers = [st.radio(f"PHQ{i+1}: {q}", ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}") for i, q in enumerate(phq_q)]
    phq_score = sum([{"Not at all":0, "Several days":1, "More than half":2, "Nearly every day":3}[a] for a in phq_answers])

with tab2:
    wem_q = ["Optimistic about the future", "Feeling useful", "Feeling relaxed", "Interested in other people", "Energy to spare", "Dealing with problems well", "Thinking clearly", "Feeling good about myself", "Feeling close to other people", "Feeling confident", "Feeling loved", "Able to make up my own mind", "Interested in new things", "Feeling cheerful"]
    wem_answers = [st.radio(f"WEM{i+1}: {q}", ["None", "Rarely", "Sometimes", "Often", "Always"], key=f"w{i}") for i, q in enumerate(wem_q)]
    wem_score = sum([{"None":1, "Rarely":2, "Sometimes":3, "Often":4, "Always":5}[a] for a in wem_answers])

with tab3:
    st.write("ISEL-12 Social Support Score (Reverse scoring handled automatically)")
    isel_items = [
        ("I’d have a hard time finding someone to go on a trip with me.", "Tangible"),
        ("There is no one I can share my most private worries with.", "Appraisal"),
        ("If I were sick, I could easily find help with chores.", "Tangible"),
        ("I have someone to turn to for advice about family problems.", "Appraisal"),
        ("I could easily find someone to go to a movie with.", "Belonging"),
        ("When I need suggestions for a personal problem, I have someone to turn to.", "Appraisal"),
        ("I don’t often get invited to do things with others.", "Belonging"),
        ("If I went out of town, someone would look after my house.", "Tangible"),
        ("If I wanted lunch, I could easily find someone to join me.", "Belonging"),
        ("If I was stranded, someone would come and get me.", "Tangible"),
        ("If a crisis arose, it would be hard to find advice.", "Appraisal"),
        ("If I needed help moving, I’d have a hard time finding help.", "Tangible")
    ]
    isel_ans = []
    for i, (q, cat) in enumerate(isel_items):
        a = st.selectbox(q, ["Definitely False", "Probably False", "Probably True", "Definitely True"], key=f"i{i}")
        val = {"Definitely False":1, "Probably False":2, "Probably True":3, "Definitely True":4}[a]
        # Reverse Score Logic
        if any(word in q.lower() for word in ["hard time", "no one", "don’t often"]):
            val = 5 - val
        isel_ans.append({'cat': cat, 'score': val})
    
    cat_scores = {c: sum([item['score'] for item in isel_ans if item['cat'] == c]) for c in ["Tangible", "Appraisal", "Belonging"]}

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

# --- LOGIC-HEAVY REPORT ---
if st.button("Generate Comprehensive 2-Part Report"):
    st.divider()
    
    # PART 1: THE STRUGGLE PROFILE
    st.title("📋 Part 1: Participant Struggle Profile")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.subheader("🔴 Immediate Risks")
        if phq_answers[8] != "Not at all": st.error("Suicide Ideation Flagged (PHQ-9 Q9)")
        if st.session_state.living in ["Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"]: st.error(f"Unstable Housing: {st.session_state.living}")
        if st.session_state.needs == "Yes": st.error("Basic Needs Deficiency (Food/Medical/Housing)")
        
    with c2:
        st.subheader("🟡 Functional Barriers")
        if phq_score >= 10: st.warning(f"Moderate to Severe Depression ({phq_score})")
        if st.session_state.emp_status == "Unemployed": st.warning("Vocational Instability")
        if cat_scores['Tangible'] <= 10: st.warning("Critical Lack of Physical Support (Rides/Chores)")
        
    with c3:
        st.subheader("🔵 Growth & Wellness")
        if wem_score < 40: st.info(f"Low Mental Well-being ({wem_score})")
        if cat_scores['Appraisal'] <= 10: st.info("Lack of Confidant/Advice")
        if cat_scores['Belonging'] <= 10: st.info("High Social Isolation")

    st.divider()

    # PART 2: TACTICAL SERVICE PLAN
    st.title("🛠️ Part 2: Tactical Service Plan")
    st.write("Review these actions with the Participant and select priorities.")
    
    # SME SECTION
    st.header("🏢 Case Management (SME Focus)")
    with st.expander("View Systemic & Resource Actions", expanded=True):
        if st.session_state.living in ["Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"]:
            st.write("👉 **HOUSING:** Immediate referral to SSVF or HUD-VASH; coordinate emergency lodging voucher.")
        if "VA Pension" not in st.session_state.income_src and "Disability related income" not in st.session_state.income_src:
            st.write("👉 **BENEFITS:** Schedule meeting with VSO; explore PACT Act eligibility to increase financial floor.")
        if phq_score >= 15:
            st.write("👉 **CLINICAL:** Warm hand-off to VA Mental Health or community clinical partner for diagnostic evaluation.")
        if st.session_state.emp_status == "Unemployed":
            st.write("👉 **VOCATIONAL:** Connect with DVOP (Disabled Veterans' Outreach Program) or local Workforce Center.")

    # PEER SECTION
    st.header("🤝 Peer Support (Battle Buddy Focus)")
    with st.expander("View Relational & Logistical Actions", expanded=True):
        if cat_scores['Tangible'] <= 10:
            st.write("👉 **LOGISTICS:** Peer to provide direct transportation to next 3 medical/benefit appointments.")
        if wem_answers[1] in ["None", "Rarely"]:
            st.write("👉 **PURPOSE:** Conduct 'Values Identification' exercise; find one small community task where Participant can contribute.")
        if cat_scores['Belonging'] <= 10:
            st.write("👉 **CONNECTION:** Peer to accompany Participant to a 'neutral' social environment (Veteran coffee, gym, or hobby group).")
        if cat_scores['Appraisal'] <= 10:
            st.write("👉 **TRUST:** Establish daily 5-minute 'no-agenda' check-ins to build rapport and confidant status.")
        if st.session_state.stress >= 7:
            st.write("👉 **STRESS REDUCTION:** Peer
