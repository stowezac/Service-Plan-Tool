import streamlit as st

st.set_page_config(page_title="Veteran Service Plan Tool", layout="wide")

st.title("Veteran Participant Success Tool")
st.write("Enter the answers exactly as they appear on the paper forms to generate a Service Plan Report.")

# --- TABS FOR ORGANIZED ENTRY ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9 (Mood)", "WEMWBS (Well-being)", "ISEL-12 (Social)", "SES (Socio-Economic)"])

# --- TAB 1: PHQ-9 ---
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
    wem_questions = [
        "Optimistic about the future", "Feeling useful", "Feeling relaxed", 
        "Interested in other people", "Energy to spare", "Dealing with problems well",
        "Thinking clearly", "Feeling good about myself", "Feeling close to other people",
        "Feeling confident", "Feeling loved", "Able to make up my own mind",
        "Interested in new things", "Feeling cheerful"
    ]
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
    isel_options = {"Definitely False": 1, "Probably False": 2, "Probably True": 3, "Definitely True": 4}

    for i, (q, category) in enumerate(isel_questions):
        ans = st.selectbox(q, isel_options.keys(), key=f"isel_{i}")
        score = isel_options[ans]
        
        # Scoring logic: some questions are 'reverse scored' (negative framing)
        if "hard time" in q or "no one" in q or "difficult" in q or "don't often" in q:
            score = 5 - score
        
        isel_scores[category] += score

# --- TAB 4: SES ---
with tab4:
    st.header("SES: Socio-Economic Status")
    income_sources = st.multiselect("Regular sources of income:", ["Disability", "VA Pension", "Employment", "Savings", "Other"])
    emp_status = st.selectbox("Current employment status:", ["Employed", "Unemployed", "Disabled", "Retired"])
    needs_struggle = st.radio("Difficulty covering medical, food, and housing?", ["No", "Yes"])
    income_reduced = st.radio("Has your income been reduced?", ["No", "Yes"])
    stress = st.radio("Experiencing stress over financial situation?", ["No", "Yes"])

# --- GENERATE REPORT BUTTON ---
if st.button("Generate Final Service Plan Report"):
    st.divider()
    st.subheader("PARTICIPANT INSIGHT REPORT")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Assessment Totals")
        st.write(f"**PHQ-9 Score:** {phq_total}")
        st.write(f"**Well-being (WEMWBS) Score:** {wem_total}")
        st.write(f"**Social Support (ISEL-12) Score:** {sum(isel_scores.values())}")

    with col2:
        st.write("### Clinical & Social Insights")
        if phq_q9 > 0:
            st.error("!! CRITICAL: Thoughts of self-harm reported. Immediate Safety Plan review required.")
        if isel_scores['Appraisal'] < 8:
            st.warning("* Peer Focus: Veteran lacks a confidant for advice. Build trust-based mentoring.")
        if isel_scores['Tangible'] < 8:
            st.warning("* Resource Focus: High need for physical/logistical help (transportation/housing).")

    st.write("### Economic Roadmap")
    if needs_struggle == "Yes":
        st.error("* URGENT: Basic needs not being met. Immediate referral to food/housing assistance.")
    if income_reduced == "Yes":
        st.info("* Action: Significant income drop detected. Refer for VA Benefits review and Financial Counseling.")
