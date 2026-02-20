import streamlit as st

st.set_page_config(page_title="Veteran Service Plan Tool", layout="wide")

st.title("Veteran Participant Success Tool")
st.write("Complete the assessment to generate a Comprehensive Priority-Based Service Plan.")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9", "WEMWBS", "ISEL-12", "SES"])

# --- TAB 1: PHQ-9 ---
with tab1:
    st.header("PHQ-9: Depressive Symptoms")
    phq_questions = ["Little interest or pleasure", "Feeling down/depressed", "Sleep issues", "Energy issues", "Appetite issues", "Feeling like a failure", "Concentration issues", "Slow/fidgety movement", "Self-harm thoughts"]
    phq_answers = []
    opts = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
    for i, q in enumerate(phq_questions):
        ans = st.radio(f"{i+1}. {q}", opts.keys(), key=f"phq_{i}", horizontal=True)
        phq_answers.append(opts[ans])
    phq_total = sum(phq_answers)
    phq_q9 = phq_answers[8]

# --- TAB 2: WEMWBS ---
with tab2:
    st.header("WEMWBS: Well-being")
    wem_questions = ["Optimistic", "Useful", "Relaxed", "Interested in others", "Energy", "Problem-solving", "Clear thinking", "Self-worth", "Closeness", "Confidence", "Feeling loved", "Decision making", "New things", "Cheerful"]
    wem_answers = []
    wem_opts = {"None": 1, "Rarely": 2, "Sometimes": 3, "Often": 4, "Always": 5}
    for i, q in enumerate(wem_questions):
        ans = st.radio(f"{i+1}. {q}", wem_opts.keys(), key=f"wem_{i}", horizontal=True)
        wem_answers.append(wem_opts[ans])
    wem_total = sum(wem_answers)

# --- TAB 3: ISEL-12 ---
with tab3:
    st.header("ISEL-12: Social Support")
    isel_questions = [
        ("Hard time finding someone for a trip", "Tangible"), ("No one for private worries", "Appraisal"),
        ("Find help with chores", "Tangible"), ("Advice for family problems", "Appraisal"),
        ("Find someone for a movie", "Belonging"), ("Suggestions for problems", "Appraisal"),
        ("Not invited to things", "Belonging"), ("Someone look after house", "Tangible"),
        ("Find lunch companion", "Belonging"), ("Stranded/Get a ride", "Tangible"),
        ("Crisis/Hard to find advice", "Appraisal"), ("Help moving/Hard time", "Tangible")
    ]
    isel_scores = {"Appraisal": 0, "Belonging": 0, "Tangible": 0}
    isel_opts = {"Definitely False": 1, "Probably False": 2, "Probably True": 3, "Definitely True": 4}
    for i, (q, cat) in enumerate(isel_questions):
        ans = st.selectbox(q, isel_opts.keys(), key=f"isel_{i}")
        score = isel_opts[ans]
        if any(x in q.lower() for x in ["hard time", "no one", "crisis", "not invited"]):
            score = 5 - score
        isel_scores[cat] += score

# --- TAB 4: SES ---
with tab4:
    st.header("SES: Socio-Economic Status")
    income_sources = st.multiselect("What are your regular sources of income? [Select all that apply]", 
                                    ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement benefits", "Employment", "Temporary Financial Assistance", "Other"])
    emp_status = st.selectbox("Current employment status:", ["Employed", "Unemployed", "Disabled", "Retired"])
    needs_struggle = st.radio("Difficulty covering medical, food, and housing?", ["No", "Yes"])
    income_reduced = st.radio("Has your income been reduced by $30k+ recently?", ["No", "Yes"])
    stress = st.radio("Is the Veteran experiencing significant financial stress?", ["No", "Yes"])

# --- ADVANCED REPORT GENERATION ---
if st.button("Generate Detailed Service Plan"):
    st.divider()
    st.title("Veteran Service Plan: Detailed Triage")
    
    # 1. IMMEDIATE SAFETY & STABILITY (Red Section)
    with st.expander("🔴 IMMEDIATE INTERVENTION (Priority 1)", expanded=True):
        if phq_q9 > 0:
            st.error(f"**SAFETY ALERT:** Participant scored {phq_q9} on Self-Harm thoughts. Action: Immediate safety planning and suicide prevention protocol.")
        if needs_struggle == "Yes":
            st.error("**STABILITY ALERT:** Basic needs (Food/Housing/Medical) are compromised. Action: Emergency warm hand-off to resources is the top priority.")
        if phq_total >= 20:
            st.error(f"**CLINICAL ALERT:** Severe Depression Score ({phq_total}). Immediate referral for clinical diagnostic assessment.")

    # 2. ECONOMIC RECOVERY (Yellow Section)
    with st.expander("🟡 ECONOMIC & RESOURCE ROADMAP (Priority 2)", expanded=True):
        if emp_status == "Unemployed":
            st.warning("**VOCATIONAL:** Veteran is currently unemployed. Suggest warm hand-off to VRE or local job placement.")
        if income_reduced == "Yes":
            st.warning("**FINANCIAL:** Significant income drop detected. Refer for VA Benefits review and Financial Literacy counseling.")
        if "Employment" not in income_sources and emp_status == "Unemployed":
            st.warning("**BENEFITS:** No employment income reported. Check eligibility for unemployment or temporary financial assistance.")

    # 3. PEER SUPPORT & SOCIAL (Blue Section)
    with st.expander("🔵 PEER SUPPORT & CONNECTION (Priority 3)", expanded=True):
        # ISEL Logic
        if isel_scores['Tangible'] <= 6:
            st.info("**TANGIBLE SUPPORT:** Veteran lacks physical help. Peer Support should help with logistical navigation (appointments, paperwork).")
        if isel_scores['Appraisal'] <= 6:
            st.info("**EMOTIONAL TRUST:** Veteran feels they have no one for advice. Peer Support Specialist should focus on building a 'Confidant' relationship.")
        if isel_scores['Belonging'] <= 6:
            st.info("**SOCIAL BELONGING:** Veteran feels excluded. Recommend Veteran-specific social groups to combat isolation.")
        
        # WEMWBS Logic
        if wem_total < 40:
            st.info(f"**WELL-BEING:** Low flourish score ({wem_total}). Recommend 'Meaning & Purpose' sessions with a Peer Specialist.")

    # 4. SUMMARY FOR CASE NOTES
    st.subheader("Draft Case Note (Copy/Paste)")
    summary = f"Participant presents with a PHQ-9 of {phq_total} and WEMWBS of {wem_total}. "
    if needs_struggle == "Yes": summary += "Emergency resource needs identified. "
    if phq_q9 > 0: summary += "SUICIDE RISK IDENTIFIED. "
    st.text_area("Summary", summary + "Service plan focuses on stabilizing immediate needs before moving to social integration goals.")
