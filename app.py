import streamlit as st

st.set_page_config(    
    page_title="VisibleHand ROI Calculator",
    page_icon="✋",
    # layout="wide"
)

minutes_per_hour = 60
hours_per_day = 24
days_per_year = 365

st.title("VisibleHand: ROI Calculator")

st.header("Please adjust inputs to see the effect on your ROI.")

st.text("(All calculations are for a single facility.)")

st.write(" ")

with st.beta_expander("Basic Inputs (expand to modify)", True):

    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])

    with slider_col:

        num_facility_patients = st.number_input('Number of patients in your facility', value=100, step=10, format='%d')
        st.write(" ")

        patients_per_unit = st.slider('Average number of patients per unit in your facilities (20 is typical)', 5, 30, 20)
        st.write(" ")

        rounding_minutes = st.slider('Average # of minutes it takes to complete each round with paper (20 patients in a unit typically takes 12-14 minutes)', 3, 20, 13)
        st.write(" ")

        time_savings_perc = st.slider('Expected % reduction in rounding time (Note: our app typically results a savings of 30%-50%.)', 10, 70, 40, 5)

st.markdown(f"**{num_facility_patients}** patients with approximiately **{patients_per_unit}** per unit, **{rounding_minutes}** minutes to complete rounding.")

st.write(" ")


with st.beta_expander("Health Tech Efficiency", False):

    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])

    with slider_col:
        staff_hourly_cost = st.slider("Full hourly dollar cost of a health tech staff member (Average hourly wage is $14, which is about $18.2 with a 30% overhead).", 10, 25, 18)    

        staff_q_time_str = st.selectbox('How often do staff rounds occur (hosptials usually do Q-15s)?', ('15 minutes', '30 minutes', '60 minutes', '90 minutes', '120 minutes'))
        staff_q_time = int(staff_q_time_str.split(" ")[0])

        staff_rounds_per_day = (minutes_per_hour * hours_per_day) / staff_q_time
        mins_saved_per_round = rounding_minutes * time_savings_perc / 100
        staff_mins_saved_per_year_per_unit = mins_saved_per_round * staff_rounds_per_day * days_per_year 
        staff_hours_saved_per_year_per_unit = staff_mins_saved_per_year_per_unit / minutes_per_hour
        staff_hours_saved_per_year_per_facility = staff_hours_saved_per_year_per_unit * (num_facility_patients / patients_per_unit)

expected_savings_staff = round(staff_hours_saved_per_year_per_facility * staff_hourly_cost)
st.markdown(f"Expected savings = **{int(round(staff_hours_saved_per_year_per_facility, 0))}** health tech hours = **${expected_savings_staff}** saved per year.")

st.write(" ")

with st.beta_expander("Nurse Efficiency"):
    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])

    with slider_col:    
        nurses_do_rounding = st.checkbox("Nurses do safety rounds (and review staff rounds)", True)
        if nurses_do_rounding:
            nurse_cost = st.slider("Full hourly dollar cost of a nurse (Average hourly wage is $31.63, which is about $41 with a 30% overhead).", 20, 60, 41, key='nurse_cost')

            nurse_q_time_str = st.selectbox('How often do nurse rounds occur (hosptials usually do every 1 or 2 hours)?', ('1 hour', '2 hours', '3 hours', '4 hours', '6 hours'), key="nurse_freq")
            nurse_q_hours = int(nurse_q_time_str.split(" ")[0])

            nurse_rounds_per_day = hours_per_day / nurse_q_hours
            nurse_mins_saved_per_round = rounding_minutes * time_savings_perc / 100
            nurse_minutes_saved_per_year_per_unit = mins_saved_per_round * nurse_rounds_per_day * days_per_year 
            nurse_hours_saved_per_year_per_unit = nurse_minutes_saved_per_year_per_unit / minutes_per_hour
            nurse_hours_saved_per_year_per_facility = nurse_hours_saved_per_year_per_unit * (num_facility_patients / patients_per_unit)

if nurses_do_rounding:
    expected_savings_nurses = round(nurse_hours_saved_per_year_per_facility * staff_hourly_cost)
    st.markdown(f"Expected savings = **{int(round(nurse_hours_saved_per_year_per_facility, 0))}** nurse hours = **${expected_savings_nurses}** saved per year.")
else:
    expected_savings_nurses = 0
    st.markdown("Savings: not applicable")

st.write(" ")

with st.beta_expander("Paper Management Reduction"):
    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])

    with slider_col:
        paper_cost = st.slider("Cost per year, in THOUSANDS, for paper, ink, printer, distribution, filing, scanning, and uploading. Average is $12K/year).", 0, 30, 12)
        paper_cost = paper_cost * 1000

expected_savings_paper = paper_cost        
st.markdown(f"Expected savings = **${expected_savings_paper}**")

st.write(" ")
st.write(" ")

include_verification = st.checkbox("Include Automated Verification in Risk and Cost Analysis", True)

with st.beta_expander("Risk and Cost of Citations"):
    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])

    with slider_col:    
        citation_cost = st.slider("Total $ cost of a citation related to safety rounding issues, including time and wages related to P.O.C., effect on reputation, etc.", 0, 200000, 50000, 10000)
        citation_risk = st.slider("Current annual % risk of a citation related to safety rounding issues (average, based on published data, is [5%])", 0, 100, 10, 5)
        if include_verification:
            citation_risk_reduction = st.slider("Estimated % risk reduction from 99% compliance AND automated proximity verification for all safety checks.", 0, 100, 90, 5)
        else:
            citation_risk_reduction = st.slider("Estimated % risk reduction from 99% safety rounding compliance", 0, 100, 50, 5)

expected_cost_citation_now = citation_cost * citation_risk / 100
expected_cost_reduction_citation = expected_cost_citation_now * citation_risk_reduction / 100
st.markdown(f"Expected reduction = **${expected_cost_reduction_citation}**")

with st.beta_expander("Risk and Cost of Litigation"):
    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])

    with slider_col:    
        litigation_cost = st.slider("Total $ cost of litigation related to safety rounding issues (note: average is difficult to estimate due to the number of cases that are settled in order to avoid publicity).", 10000, 1000000, 100000, 100000)
        litigation_risk = st.slider("Current annual % risk of litigation related to safety rounding issues (note: average is difficult to estimate due to the number of cases that are settled in order to avoid publicity)", 0, 100, 5, 5)
        if include_verification:
            litigation_risk_reduction = st.slider("Estimated % risk reduction from 99% compliance AND automated proximity verification for all safety checks.", 0, 100, 90, 5, key='risk_reduction_lit_ver')
        else:
            litigation_risk_reduction = st.slider("Estimated % risk reduction from 99% safety rounding compliance", 0, 100, 50, 5, key='risk_reduction_lit_comp')

expected_cost_litigation_now = litigation_cost * litigation_risk / 100
expected_cost_reduction_litigation = expected_cost_litigation_now * litigation_risk_reduction / 100
st.markdown(f"Expected reduction = **${expected_cost_reduction_litigation}**")

st.write(" ")
st.write(" ")
st.header("ROI")
if include_verification:
    cost = 65 * num_facility_patients * 12
else:
    cost = 25 * num_facility_patients * 12
st.markdown(f"Annual recurring cost of VisibleHand system and hardware = **${cost}**")

total_savings = expected_savings_staff + expected_savings_nurses + expected_savings_paper + expected_cost_reduction_citation + expected_cost_reduction_litigation
st.markdown(f"Annual expected savings = **${total_savings}**")

roi = total_savings / cost
# st.markdown(f"ROI = **{round(roi, 1)}**")

# Risk of litigation

# Average full cost when litigation occurs
#(Link to article showing highest known incident)



