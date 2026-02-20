import streamlit as st

st.set_page_config(page_title="Veteran Participant Success Tool", layout="wide")

st.title("Veteran Participant Success Tool")
st.write("Complete the assessment to generate a Priority-Based Service Plan.")

# --- TABS FOR ENTRY ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9", "WEMWBS", "ISEL-12", "SES"])

# --- TAB 1: PHQ-9 (Original Order) ---
with tab1:
    st.header("PHQ-9: Depressive Symptoms")
    phq_questions = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself — or that you are a failure",
        "Trouble concentrating on things (reading, TV)",
        "Moving or speaking so slowly... or being fidgety/restless",
        "Thoughts that you would be better off dead or hurting yourself"
    ]
    phq_answers = []
    options = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
    for i, q in enumerate(phq_questions):
        ans = st.radio(f"{i+1}. {q}", options.keys(), key=f"phq_{i}", horizontal=True)
        phq_answers.append(options[ans])
    phq_total = sum(phq_answers)
    phq_q9 = phq_answers[8]

# --- TAB 2: WEMWBS ---
with tab2:
    st.header("WEMWBS: Mental Well-being")
    wem_questions = ["Optimistic about the future", "Feeling useful", "Feeling relaxed", "Interested in other people", "Energy to spare", "Dealing with problems well", "Thinking clearly", "Feeling good about myself", "Feeling close to other people", "Feeling confident", "Feeling loved", "Able to make up my own mind", "Interested in new things", "Feeling cheerful"]
    wem_answers = []
    wem_options = {"None of the time": 1, "Rarely": 2, "Some of the time": 3, "Often": 4, "All of the time": 5}
    for i, q in enumerate(wem_questions):
        ans = st.radio(f"I've been... {q}", wem_options.keys(), key=f"wem_{i}", horizontal=True)
        wem_answers.append(wem_options[ans])
    wem_total = sum(wem_answers)

# --- TAB 3: ISEL-12 ---
with tab3:
    st.header("ISEL-12: Social Support")
    isel_questions = [
        ("I'd have a hard time finding someone to go on a trip with me.", "Tangible"),
        ("There is no one I can share my most private worries with.", "Appraisal"),
        ("If I were sick, I could easily find help with chores.", "Tangible"),
        ("I have someone to turn to for advice about family problems.", "Appraisal"),
        ("I could easily find someone to go to a movie with.", "Belonging"),
        ("When I need suggestions for a personal problem, I have someone to turn to.", "Appraisal"),
        ("I don't often get invited to do things with others.", "Belonging"),
        ("If I went out of town, someone would look after my house.", "Tangible"),
        ("If I wanted lunch, I could easily find someone to join me.", "Belonging"),
        ("If I was stranded, someone would come and get me.", "Tangible"),
        ("If a crisis arose, it would be hard to find advice.", "Appraisal"),
        ("If I needed help moving, I'd have a hard time finding help.", "Tangible")
    ]
    isel_scores = {"Appraisal": 0, "Belonging": 0, "Tangible": 0}
    isel_opts = {"Definitely False": 1, "Probably False": 2, "Probably True": 3, "Definitely True": 4}
    for i, (q, cat) in enumerate(isel_questions):
        ans = st.selectbox(q, isel_opts.keys(), key=f"isel_{i}")
        score = isel_opts[ans]
        if any(word in q.lower() for word in ["hard time", "no one", "difficult", "don't often"]):
            score = 5 - score
        isel_scores[cat] += score

# --- TAB 4: SES ---
with tab4:
    st.header("SES: Socio-Economic Status")
    emp_status = st.selectbox("Current employment status:", ["Employed", "Unemployed", "Disabled", "Retired"])
    needs_struggle = st.radio("Difficulty covering medical, food, and housing?", ["No", "Yes"])
    income_reduced = st.radio("Has your income been reduced by $30k+ recently?", ["No", "Yes"])
    stress = st.radio("Is the Veteran experiencing significant financial stress?", ["No", "Yes"])

# --- REPORT GENERATION ---
if st.button("Generate High-Priority Service Plan"):
    st.divider()
    st.title("PARTICIPANT SERVICE PLAN & TRIAGE REPORT")

    # PRIORITY 1: IMMEDIATE INTERVENTION (RED)
    st.error("### 🔴 PRIORITY 1: IMMEDIATE INTERVENTION")
    p1_count = 0
    if phq_q9 > 0:
        st.write("**CRITICAL: Suicide Risk Detected.** Participant indicated thoughts of self-harm. Action: Immediate Safety Plan and clinical escalation.")
        p1_count += 1
    if needs_struggle == "Yes":
        st.write("**STABILITY: Basic Needs Gap.** Difficulty with food, housing, or medical. Action: Emergency resource warm hand-off (Food bank, HUD-VASH, etc.).")
        p1_count += 1
    if p1_count == 0: st.write("*No Priority 1 issues identified.*")

    # PRIORITY 2: STRATEGIC STABILIZATION (YELLOW)
    st.warning("### 🟡 PRIORITY 2: STRATEGIC STABILIZATION")
    p2_count = 0
    if phq_total >= 15:
        st.write(f"**MENTAL HEALTH: Severe Depression (Score: {phq_total}).** Participant is highly symptomatic. Action: Refer to clinical counseling.")
        p2_count += 1
    if emp_status == "Unemployed":
        st.write("**ECONOMIC: Lack of Employment.** Action: Refer to vocational training or VA employment representative.")
        p2_count += 1
    if isel_scores['Tangible'] <= 6:
        st.write("**SOCIAL: Low Tangible Support.** Lacks physical help (rides, chores). Action: Peer support to assist with logistics.")
        p2_count += 1
    if p2_count == 0: st.write("*No Priority 2 issues identified.*")

    # PRIORITY 3: PEER SUPPORT & CONNECTION (BLUE)
    st.info("### 🔵 PRIORITY 3: PEER SUPPORT & CONNECTION")
    p3_count = 0
    if wem_total < 40:
        st.write(f"**WELL-BEING: Low Mental Flourishing (Score: {wem_total}).** Action: Assign Peer Specialist for optimism-building and 'Value' check-ins.")
        p3_count += 1
    if isel_scores['Belonging'] <= 6:
        st.write("**SOCIAL: Isolation.** Lacks people to do things with. Action: Invite to Veteran social cohorts or group activities.")
        p3_count += 1
    if isel_scores['Appraisal'] <= 6:
        st.write("**SOCIAL: No Confidant.** Lacks someone for advice. Action: Focus Peer Specialist relationship on building deep trust.")
        p3_count += 1
    if p3_count == 0: st.write("*No Priority 3 issues identified.*")

    st.divider()
    st.write("**Manager Notes:** Use this priority list to guide the warm hand-offs. Address Red flags first before moving to social or well-being goals.")
