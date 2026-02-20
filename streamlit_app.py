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
    phq_q = ["Little interest or pleasure", "Feeling down, depressed, hopeless", "Trouble sleeping", "Feeling tired/little energy", "Poor appetite/overeating", "Feeling like a failure", "Trouble concentrating", "Moving slowly/Fidgety", "Thoughts of self-harm"]
    phq_answers = [st.radio(f"PHQ{i+1}: {q}", ["Not at all", "Several days", "More than half", "Nearly every day"], key=f"p{i}") for i, q in enumerate(phq_q)]
    phq_score = sum([{"Not at all":0, "Several days":1, "More than half":2, "Nearly every day":3}[a] for a in phq_answers])

with tab2:
    wem_q = ["Optimistic", "Feeling useful", "Feeling relaxed", "Interested in people", "Energy to spare", "Dealing with problems", "Thinking clearly", "Feeling good about myself", "Feeling close to people", "Feeling confident", "Feeling loved", "Decision making", "New things", "Feeling cheerful"]
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
        ("If I
