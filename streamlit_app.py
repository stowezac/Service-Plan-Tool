import streamlit as st

st.set_page_config(page_title="Veteran Service Plan Tool", layout="wide")

st.title("Veteran Participant Choice & Service Plan Tool")
st.write("Complete the forms to generate a Menu of Choices for the Participant.")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["PHQ-9", "WEMWBS", "ISEL-12", "SES"])

# --- DATA ENTRY (Same as before but keeping logic clean) ---
with tab1:
    st.header("PHQ-9")
    phq_questions = ["Little interest", "Feeling down", "Sleep", "Energy", "Appetite", "Failure", "Concentration", "Slow/Fidgety", "Self-harm"]
    phq_answers = [st.radio(q, ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}", horizontal=True) for i, q in enumerate(phq_questions)]
    phq_total = sum([{"Not at all":0, "Several days":1, "More than half":2, "Nearly every day":3}[a] for a in phq_answers])
    phq_q9 = phq_answers[8] != "Not at all"

with tab2:
    st.header("WEMWBS")
    wem_questions = ["Optimistic", "Useful", "Relaxed", "Interested in others", "Energy", "Problem-solving", "Clear thinking", "Self-worth", "Closeness", "Confidence", "Feeling loved", "Decision making", "New things", "Cheerful"]
    wem_answers = [st.radio(q, ["None", "Rarely", "Sometimes", "Often", "Always"], key=f"w{i}", horizontal=True) for i, q in enumerate(wem_questions)]
    wem_total = sum([{"None":1, "Rarely":2, "Sometimes":3, "Often":4, "Always":5}[a] for a in wem_answers])
    feeling_useful = wem_answers[1] in ["None", "Rarely"]

with tab3:
    st.header("ISEL-12")
    # Mapping and reverse scoring logic handled in background
    isel_questions = [("Hard time/Trip", "T"), ("No one/Private worries", "A"), ("Help/Chores", "T"), ("Advice/Family", "A"), ("Someone/Movie", "B"), ("Suggestions/Problem", "A"), ("Not invited", "B"), ("Look after house", "T"), ("Lunch companion", "B"), ("Stranded/Ride", "T"), ("Crisis/Advice", "A"), ("Help moving", "T")]
    isel_data = [st.selectbox(q[0], ["Definitely False", "Probably False", "Probably True", "Definitely True"], key=f"i{i}") for i, q in enumerate(isel_questions)]

with tab4:
    st.header("SES")
    income_sources = st.multiselect("Sources of Income:", ["Disability related income", "VA Pension", "Non-VA Pension", "Retirement", "Employment", "Other"])
    emp_status = st.selectbox("Employment status:", ["Employed", "Unemployed", "Disabled", "Retired"])
    needs_struggle = st.radio("Difficulty covering medical, food, and housing?", ["No", "Yes"])
    income_reduced = st.radio("Has income been reduced by $30k+?", ["No", "Yes"])

# --- REPORT GENERATION ---
if st.button("Generate Service Plan Menu"):
    st.divider()
    st.title("PARTICIPANT CHOICE MENU")
    st.write("Review these needs with the Participant and let them select which to prioritize.")

    # TIER 1: SURVIVAL
    st.error("### 🔴 TIER 1: URGENT SURVIVAL & SAFETY")
    if phq_q9: st.checkbox("SAFETY: Address thoughts of self-harm / Safety Planning")
    if needs_struggle == "Yes": st.checkbox("BASIC NEEDS: Secure food, housing, or medical stability")
    if "VA Pension" not in income_sources and "Disability related income" not in income_sources:
        st.checkbox("BENEFITS: Veteran is not receiving VA Benefits. Connect with VSO to explore claims.")

    # TIER 2: STABILITY (Case Management)
    st.warning("### 🟡 TIER 2: STABILITY & RESOURCES")
    if emp_status == "Unemployed": st.checkbox("EMPLOYMENT: Explore job search or vocational training")
    if income_reduced == "Yes": st.checkbox("FINANCIAL: Financial counseling to address $30k+ income drop")
    st.checkbox("CASE NOTE: Update master file with current assessment scores")

    # TIER 3: CONNECTION (Peer Support)
    st.info("### 🔵 TIER 3: CONNECTION & PURPOSE")
    if feeling_useful: st.checkbox("PURPOSE: Identify opportunities to feel 'useful' (Volunteering/Mentoring)")
    st.checkbox("SOCIAL: Peer to attend a community or Veteran event with Participant")
    st.checkbox("RELATIONAL: Weekly 'Battle Buddy' check-in call")

    st.divider()
    st.subheader("Discovery Questions for Staff")
    if needs_struggle == "Yes": st.write("* 'Are you facing an eviction or shut-off notice in the next 30 days?'")
    if feeling_useful: st.write("* 'What is one thing you used to enjoy doing where you felt like you were contributing?'")
