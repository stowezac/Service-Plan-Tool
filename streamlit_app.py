import streamlit as st
import random

st.set_page_config(page_title="SSG Fox Participant Tool", layout="wide")

# --- SESSION STATE FOR RANDOMIZATION ---
if 'random_data' not in st.session_state:
    st.session_state.random_data = False

def randomize():
    st.session_state.random_data = True

st.title("Veteran Participant Success Tool (Full Version)")
st.button("🎲 Randomize Answers (For Testing)", on_click=randomize)

# --- HELPERS ---
def get_val(options, index_override=0):
    if st.session_state.random_data:
        return random.choice(options)
    return options[index_override]

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9", "WEMWBS", "ISEL-12", "Full SES"])

# --- TAB 1: PHQ-9 ---
with tab1:
    st.header("PHQ-9: Mood & Safety")
    phq_q = ["Little interest/pleasure", "Feeling down/depressed", "Sleep issues", "Energy issues", "Appetite issues", "Feeling failure", "Concentration", "Slow/Fidgety", "Self-harm thoughts"]
    phq_opts = ["Not at all", "Several days", "More than half", "Nearly every day"]
    phq_answers = [st.radio(q, phq_opts, index=phq_opts.index(get_val(phq_opts)) if st.session_state.random_data else 0, key=f"p{i}") for i, q in enumerate(phq_q)]
    phq_total = sum([phq_opts.index(a) for a in phq_answers])
    phq_q9 = phq_answers[8] != "Not at all"

# --- TAB 2: WEMWBS ---
with tab2:
    st.header("WEMWBS: Well-being")
    wem_q = ["Optimistic", "Useful", "Relaxed", "Interested in others", "Energy", "Problem solving", "Thinking clearly", "Self-worth", "Closeness", "Confidence", "Loved", "Decision making", "New things", "Cheerful"]
    wem_opts = ["None", "Rarely", "Sometimes", "Often", "Always"]
    wem_answers = [st.radio(q, wem_opts, index=wem_opts.index(get_val(wem_opts)) if st.session_state.random_data else 0, key=f"w{i}") for i, q in enumerate(wem_q)]
    wem_total = sum([wem_opts.index(a)+1 for a in wem_answers])

# --- TAB 3: ISEL-12 ---
with tab3:
    st.header("ISEL-12: Social Support")
    isel_q = [("Hard time/Trip", "T"), ("No one/Private worries", "A"), ("Help/Chores", "T"), ("Advice/Family", "A"), ("Someone/Movie", "B"), ("Suggestions/Problem", "A"), ("Not invited", "B"), ("Look after house", "T"), ("Lunch companion", "B"), ("Stranded/Ride", "T"), ("Crisis/Advice", "A"), ("Help moving", "T")]
    isel_opts = ["Definitely False", "Probably False", "Probably True", "Definitely True"]
    isel_data = [st.selectbox(q[0], isel_opts, index=isel_opts.index(get_val(isel_opts)) if st.session_state.random_data else 0, key=f"i{i}") for i, q in enumerate(isel_q)]

# --- TAB 4: FULL SES ---
with tab4:
    st.header("Full Socio-Economic Status (SES)")
    col1, col2 = st.columns(2)
    with col1:
        marital = st.selectbox("Marital Status", ["Single", "Married", "Separated", "Divorced", "Widowed"], index=0 if not st.session_state.random_data else random.randint(0,4))
        living = st.selectbox("Current Living Situation", ["Renting", "Own Home", "Staying with friends/family", "Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"], index=0 if not st.session_state.random_data else random.randint(0,5))
        emp_status = st.selectbox("Employment Status", ["Employed Full-Time", "Employed Part-Time", "Unemployed", "Disabled", "Retired", "Student"], index=0 if not st.session_state.random_data else random.randint(0,5))
    with col2:
        income_sources = st.multiselect("Sources of Income", ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement", "Employment", "Social Security", "Public Assistance", "No Income"], default=[] if not st.session_state.random_data else [get_val(["Employment", "VA Pension"])])
        needs_struggle = st.radio("Difficulty covering basic needs (Food/Housing)?", ["No", "Yes"], index=0 if not st.session_state.random_data else random.randint(0,1))
        income_reduced = st.radio("Income reduced by $30k+ recently?", ["No", "Yes"], index=0 if not st.session_state.random_data else random.randint(0,1))
    
    financial_stress = st.slider("Level of financial stress (1-10)", 1, 10, 5 if not st.session_state.random_data else random.randint(1,10))

# --- GENERATE REPORT ---
if st.button("Generate Comprehensive Service Plan"):
    st.session_state.random_data = False # Reset for next use
    st.divider()
    st.title("PARTICIPANT SERVICE PLAN MENU")

    # TIER 1: CRITICAL
    st.error("### 🔴 TIER 1: IMMEDIATE NEEDS")
    if phq_q9: st.checkbox("⚠️ SAFETY: Urgent suicide risk protocol/Safety Planning required.")
    if living in ["Motel/Hotel", "Homeless Shelter", "Outdoors/Car/Bridge"]: st.checkbox(f"⚠️ HOUSING CRISIS: Participant is {living}. Immediate housing stabilization needed.")
    if needs_struggle == "Yes": st.checkbox("⚠️ BASIC NEEDS: Connect to emergency food or medical funds.")
    if "VA Pension" not in income_sources and "Disability related income" not in income_sources: st.checkbox("⚠️ BENEFITS: No VA income detected. Refer to VSO/Claims Specialist.")

    # TIER 2: STABILITY
    st.warning("### 🟡 TIER 2: RESOURCE STABILIZATION")
    if "Unemployed" in emp_status: st.checkbox("VOCATIONAL: Veteran is unemployed. Initiate job search/VRE referral.")
    if income_reduced == "Yes" or financial_stress > 7: st.checkbox("FINANCIAL: High stress/Income drop. Refer for financial literacy counseling.")
    if phq_total >= 15: st.checkbox(f"MENTAL HEALTH: High Depression Score ({phq_total}). Refer for clinical counseling.")

    # TIER 3: PEER SUPPORT
    st.info("### 🔵 TIER 3: CONNECTION & PURPOSE")
    if wem_total < 40: st.checkbox("WELL-BEING: Peer Specialist to focus on identifying 'Life Purpose' goals.")
    st.checkbox("SOCIAL: Invite to Veteran Cohort or community engagement activity.")
    st.checkbox("MENTORSHIP: Assign 'Battle Buddy' for weekly relational check-ins.")

    st.divider()
    st.subheader("Grant Metric Impact")
    st.write(f"**Well-being:** {wem_total} | **Mental Health:** {phq_total} | **Financial Stress:** {financial_stress}/10")
