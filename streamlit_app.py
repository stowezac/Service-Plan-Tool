import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(page_title="SSG Fox EHR Tool", layout="wide")

# --- STEP 1: THE DATABASE ---
# This holds the history for the Veteran
if 'veteran_db' not in st.session_state:
    st.session_state.veteran_db = []

# --- SIDEBAR: VETERAN PROFILE ---
with st.sidebar:
    st.header("👤 Veteran Profile")
    vet_name = st.text_input("Veteran Name/ID", value="Veteran-001")
    enrollment_date = st.date_input("Enrollment Date", datetime.date(2023, 1, 1))
    st.divider()
    st.info("This tool tracks progress over time to adjust the Tactical Service Plan.")

# --- APP TABS ---
tab_dashboard, tab_input = st.tabs(["📈 Progress Dashboard", "📝 Log New Assessment"])

# --- TAB: INPUT NEW DATA ---
with tab_input:
    st.header(f"New Assessment for {vet_name}")
    date_assessed = st.date_input("Assessment Date")
    assessment_type = st.selectbox("Assessment Milestone", ["Baseline", "Month 1", "Month 3", "Month 6", "Ad-hoc", "Discharge"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Clinical Scores")
        phq = st.slider("PHQ-9 Total Score", 0, 27, 10)
        wem = st.slider("WEMWBS Total Score", 14, 70, 40)
        isel = st.slider("ISEL-12 Total Score", 0, 36, 20)
        suicide_risk = st.checkbox("Thoughts of self-harm reported? (PHQ-9 Q9)")
        
    with col2:
        st.subheader("SES Indicators")
        emp_status = st.selectbox("Employment Status", ["Employed", "Unemployed", "Disabled", "Retired"])
        fin_stress = st.radio("Experiencing Financial Stress?", ["Yes", "No"])
        basic_needs = st.radio("Difficulty covering basic needs?", ["Yes", "No"])

    if st.button("Save Assessment to EHR"):
        new_entry = {
            "Date": date_assessed,
            "Milestone": assessment_type,
            "PHQ9": phq,
            "WEMWBS": wem,
            "ISEL12": isel,
            "SuicideRisk": suicide_risk,
            "Employed": emp_status,
            "FinStress": fin_stress,
            "BasicNeeds": basic_needs
        }
        st.session_state.veteran_db.append(new_entry)
        st.success("Assessment Saved!")

# --- TAB: PROGRESS DASHBOARD ---
with tab_dashboard:
    if not st.session_state.veteran_db:
        st.warning("No data found. Please log an assessment in the next tab.")
    else:
        df = pd.DataFrame(st.session_state.veteran_db).sort_values(by="Date")
        
        # 1. TREND GRAPH
        st.subheader("Clinical Trends Over Time")
        fig = px.line(df, x="Date", y=["PHQ9", "WEMWBS", "ISEL12"], 
                      title="Symptom Tracking (Lower PHQ is better, Higher WEM/ISEL is better)",
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)

        # 2. COMPARISON LOGIC (Improvement vs. Struggle)
        if len(df) >= 2:
            baseline = df.iloc[0]
            current = df.iloc[-1]
            
            st.divider()
            st.subheader("🔄 Change Analysis (Baseline vs. Current)")
            
            c1, c2, c3 = st.columns(3)
            
            # Improvement Logic
            with c1:
                st.write("### ✅ Improvements")
                if current['PHQ9'] < baseline['PHQ9']:
                    st.success(f"Depression symptoms decreased by {baseline['PHQ9'] - current['PHQ9']} points.")
                if current['Employed'] == "Employed" and baseline['Employed'] == "Unemployed":
                    st.success("Veteran successfully gained employment!")
                if current['FinStress'] == "No" and baseline['FinStress'] == "Yes":
                    st.success("Financial stress has stabilized.")

            # Ongoing/New Struggle Logic
            with c2:
                st.write("### ⚠️ Ongoing/New Struggles")
                if current['PHQ9'] >= 15:
                    st.error(f"PHQ-9 remains high ({current['PHQ9']}).")
                if current['SuicideRisk']:
                    st.error("Active Suicidal Ideation flag.")
                if current['BasicNeeds'] == "Yes":
                    st.error("Ongoing basic needs deficiency.")

            # Adjusted Service Plan
            with c3:
                st.write("### 🛠️ Adjusted Service Plan")
                if current['PHQ9'] > baseline['PHQ9']:
                    st.write("👉 **Clinical:** Escalation of care; consult with LCSW/Psychologist.")
                if current['Employed'] == "Employed":
                    st.write("👉 **Vocational:** Pivot to Job Retention and Financial Budgeting.")
                else:
                    st.write("👉 **Vocational:** Continue intensive Workforce center engagement.")
                if current['ISEL12'] < baseline['ISEL12']:
                    st.write("👉 **Peer:** Increase social outings; social support is declining.")

        # 3. RAW DATA TABLE
        st.divider()
        st.subheader("Historical Assessment Log")
        st.table(df)
