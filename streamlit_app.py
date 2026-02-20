import streamlit as st
import random

st.set_page_config(page_title="SSG Fox Participant Tool", layout="wide")

# --- FIXING THE RANDOMIZATION BUG ---
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

def fill_random():
    # PHQ-9
    for i in range(9): st.session_state[f"p{i}"] = random.choice(["Not at all", "Several days", "More than half", "Nearly every day"])
    # WEMWBS
    for i in range(14): st.session_state[f"w{i}"] = random.choice(["None", "Rarely", "Sometimes", "Often", "Always"])
    # ISEL
    for i in range(12): st.session_state[f"i{i}"] = random.choice(["Definitely False", "Probably False", "Probably True", "Definitely True"])
    # SES
    st.session_state["marital"] = random.choice(["Single", "Married", "Separated", "Divorced", "Widowed"])
    st.session_state["living"] = random.choice(["Renting", "Own Home", "Staying with friends/family", "Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"])
    st.session_state["emp_status"] = random.choice(["Employed Full-Time", "Employed Part-Time", "Unemployed", "Disabled", "Retired", "Student"])
    st.session_state["needs"] = random.choice(["No", "Yes"])
    st.session_state["income_drop"] = random.choice(["No", "Yes"])
    st.session_state["stress"] = random.randint(1, 10)

st.title("SSG Fox Participant Success Tool")
st.button("🎲 Randomize Answers for Testing", on_click=fill_random)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9 (Mood)", "WEMWBS (Well-being)", "ISEL-12 (Social)", "Full SES (Economic)"])

with tab1:
    phq_q = ["Little interest/pleasure", "Feeling down/depressed", "Sleep issues", "Energy issues", "Appetite issues", "Feeling failure", "Concentration", "Slow/Fidgety", "Self-harm thoughts"]
    phq_answers = [st.radio(q, ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}") for i, q in enumerate(phq_q)]
    phq_total = sum([{"Not at all":0, "Several days":1, "More than half":2, "Nearly every day":3}[a] for a in phq_answers])

with tab2:
    wem_q = ["Optimistic", "Useful", "Relaxed", "Interested in others", "Energy", "Problem solving", "Thinking clearly", "Self-worth", "Closeness", "Confidence", "Loved", "Decision making", "New things", "Cheerful"]
    wem_answers = [st.radio(q, ["None", "Rarely", "Sometimes", "Often", "Always"], key=f"w{i}") for i, q in enumerate(wem_q)]
    wem_total = sum([{"None":1, "Rarely":2, "Sometimes":3, "Often":4, "Always":5}[a] for a in wem_answers])

with tab3:
    isel_q = [("Hard time/Trip", "T"), ("No one/Private worries", "A"), ("Help/Chores", "T"), ("Advice/Family", "A"), ("Someone/Movie", "B"), ("Suggestions/Problem", "A"), ("Not invited", "B"), ("Look after house", "T"), ("Lunch companion", "B"), ("Stranded/Ride", "T"), ("Crisis/Advice", "A"), ("Help moving", "T")]
    isel_answers = [st.selectbox(q[0], ["Definitely False", "Probably False", "Probably True", "Definitely True"], key=f"i{i}") for i, q in enumerate(isel_q)]
    
    # Simple ISEL Logic for the report
    low_tangible = "Definitely False" in [isel_answers[0], isel_answers[2], isel_answers[7]]

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        marital = st.selectbox("Marital Status", ["Single", "Married", "Separated", "Divorced", "Widowed"], key="marital")
        living = st.selectbox("Current Living Situation", ["Renting", "Own Home", "Staying with friends/family", "Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"], key="living")
        emp_status = st.selectbox("Employment Status", ["Employed Full-Time", "Employed Part-Time", "Unemployed", "Disabled", "Retired", "Student"], key="emp_status")
    with col2:
        income_sources = st.multiselect("Sources of Income", ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement", "Employment", "Social Security", "Public Assistance", "No Income"], key="income_src")
        needs_struggle = st.radio("Difficulty covering basic needs (Food/Housing)?", ["No", "Yes"], key="needs")
        income_reduced = st.radio("Income reduced by $30k+ recently?", ["No", "Yes"], key="income_drop")
    stress = st.slider("Financial Stress Level", 1, 10, key="stress")

# --- REPORT GENERATION ---
if st.button("Generate Detailed Reports"):
    st.divider()
    
    # REPORT 1: THE STRUGGLE PROFILE
    st.title("📋 Part 1: Struggle Profile")
    st.write("This section identifies exactly where the Veteran is currently facing barriers.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("⚠️ Urgent Vulnerabilities")
        if phq_answers[8] != "Not at all": st.error("- **Active Suicide Ideation:** Positive response to PHQ-9 Q9.")
        if living in ["Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"]: st.error(f"- **Housing Crisis:** Current status is {living}.")
        if needs_struggle == "Yes": st.error("- **Survival Threat:** Unable to meet basic food/medical/housing needs.")
        
    with col_b:
        st.subheader("📉 Functional Barriers")
        if phq_total >= 15: st.warning(f"- **Clinical Depression:** PHQ-9 score is {phq_total} (Severe).")
        if emp_status == "Unemployed": st.warning("- **Vocational Gap:** Participant is currently without income-generating work.")
        if wem_total < 40: st.warning("- **Low Well-being:** Participant reports low sense of value/optimism.")

    st.divider()

    # REPORT 2: SUGGESTED ACTIONS (The Deep Dive)
    st.title("🛠️ Part 2: Tactical Service Plan")
    
    # CASE MANAGEMENT DEEP DIVE
    st.subheader("🏢 Case Management Actions (The SME)")
    with st.expander("View Case Management Tasks", expanded=True):
        if "VA Pension" not in income_sources and "Disability related income" not in income_sources:
            st.write("✅ **VA Claims:** Connect with VSO; start Intent to File for compensation/pension.")
        if living != "Renting" and living != "Own Home":
            st.write("✅ **Housing SME:** Coordinate with HUD-VASH or SSVF providers for immediate placement.")
        if phq_total >= 10:
            st.write("✅ **Clinical Referral:** Facilitate warm hand-off to VA Mental Health or community provider.")
        st.write("✅ **Resource Mapping:** Identify specific grants for temporary financial assistance (TFA).")

    # PEER SUPPORT DEEP DIVE
    st.subheader("🤝 Peer Support Actions (The Battle Buddy)")
    with st.expander("View Peer Support Tasks", expanded=True):
        if low_tangible:
            st.write("✅ **Tangible Augment:** Peer to assist with physical transport to appointments this week.")
        if wem_answers[1] in ["None", "Rarely"]: # Feeling Useful
            st.write("✅ **Purpose Building:** Peer to identify one 'small win' task or volunteer role to rebuild sense of utility.")
        if wem_total < 45:
            st.write("✅ **Battle Buddy Check-ins:** Increase frequency to 2-3 times weekly for relational grounding.")
        st.write("✅ **Social Exposure:** Accompany participant to a local Veteran coffee social or VSO meeting to reduce isolation.")

    st.divider()
    st.info("**Participant Choice Note:** Present these lists to the Veteran. Ask: 'Which of these smells like the biggest fire to you right now? That is where we start.'")
