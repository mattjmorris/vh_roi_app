import streamlit as st

st.set_page_config(    
    page_title="VisibleHand Return On Investment Calculator",
    page_icon="✋",
    # layout="wide"
)

minutes_per_hour = 60
hours_per_day = 24
days_per_year = 365

st.title("[VisibleHand](https://www.visiblehand.com/) Return On Investment")

d = """
The [VisibleHand](https://www.visiblehand.com/) digital safety solution consists of a **mobile device and app** for documenting staff safety rounds, 
and an optional **automated verification component** that ensures every patient observation occurs in person.
Expand sections on the right (click the '+') to explore the expected impact of our system on your facility.
"""
# st.sidebar.markdown("--------")
st.sidebar.info(d)

# st.sidebar.markdown("## Product Options")
st.write(" ")
st.write(" ")
# st.info("Expand sections each section below and change inputs to see the impact on your ROI.")
st.write(" ")
st.write("Do you want to include our Automated Verification component in these analyses? Automated Verification adds to the cost of the system but has a greater impact on risk reduction.")
include_verification = st.checkbox("Include automated verification component in analyses", False)

st.write(" ")
st.write(" ")

with st.beta_expander("What is your facility setup and how long do rounds take?", False):

    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])

    with slider_col:

        num_facility_patients = st.number_input('Number of patients in your facility', value=100, step=10, format='%d')
        st.write(" ")

        number_of_units = st.slider('Number of Units', 1, 20, 5)
        st.write(" ")

        mins_to_complete_round = st.slider('Average # of minutes it takes to complete each round with paper (20 patients in a unit typically takes 12 minutes)', 3, 20, 13)
        st.write(" ")


st.markdown(f"**{num_facility_patients}** patients, **{number_of_units}** units, **{mins_to_complete_round}** minutes on average to complete rounding.")

st.write(" ")
st.write(" ")
st.write(" ")


with st.beta_expander("What is the impact of increasing Health Tech efficiency?", False):

    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])

    with slider_col:  

        st.success("We find that staff typically complete their rounds 40% faster with our digital app than with paper, providing staff with time to complete other tasks.")
        
        time_savings_perc = st.slider(
            'Expected % time savings.', 
            10, 70, 40, 5
        )     
 

        staff_q_time_str = st.selectbox(
            'How often do staff rounds occur (hosptials usually do Q-15s)?', ('15 minutes', '30 minutes', '60 minutes', '90 minutes', '120 minutes')
        )
        staff_q_time = int(staff_q_time_str.split(" ")[0])

        st.write(" ")

        staff_hourly_value = st.slider(
            "Value of 1 extra hour of health tech time. (Note that the average total hourly health tech cost, including overhead, is $18.2 an hour.)", 
            0, 20, 10
        ) 

        number_of_staff_rounds_per_unit_per_day = (minutes_per_hour * hours_per_day) / staff_q_time
        mins_saved_per_round = mins_to_complete_round * time_savings_perc / 100
        staff_mins_saved_per_year_per_unit = mins_saved_per_round * number_of_staff_rounds_per_unit_per_day * days_per_year 
        staff_hours_saved_per_year_per_unit = staff_mins_saved_per_year_per_unit / minutes_per_hour
        staff_hours_saved_per_year_per_facility = staff_hours_saved_per_year_per_unit * number_of_units
        expected_savings_staff = round(staff_hours_saved_per_year_per_facility * staff_hourly_value)

        st.markdown(" ")
        t = f"""
        CALCULATIONS
        Minutes saved per round: {mins_to_complete_round} * {time_savings_perc / 100} = {round(mins_saved_per_round,1)}
        Number of rounds per unit per day: ({minutes_per_hour} * {hours_per_day}) / {staff_q_time} = {int(number_of_staff_rounds_per_unit_per_day)}
        Hours saved per unit per year: ({round(mins_saved_per_round,1)} / 60) * {int(number_of_staff_rounds_per_unit_per_day)} * 365 = {round(staff_hours_saved_per_year_per_unit,1)}
        Hours saved per facility per year: {round(staff_hours_saved_per_year_per_unit,1)} * {number_of_units} = {round(staff_hours_saved_per_year_per_facility,1)}
        Dollars saved per year = {int(round(staff_hours_saved_per_year_per_facility, 0)):,} * ${staff_hourly_value} = ${expected_savings_staff:,}
        """
        st.text(t)

st.markdown(f"`{int(round(staff_hours_saved_per_year_per_facility, 0)):,}` saved health tech hours per year at ${staff_hourly_value} value per hour = `${expected_savings_staff:,}` saved per year.")

st.write(" ")
st.write(" ")
st.write(" ")


with st.beta_expander("What is the impact of increasing Nurse efficiency?"):
    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])

    with slider_col:    
        nurses_do_rounding = st.checkbox("Nurses do safety rounds (and review staff rounds)", True)
        if nurses_do_rounding:

            st.success("Nurses save at least as much time as staff during their rounds, and usually more because reviewing staff observations is many times faster with our app than with paper.")
            st.write(" ")

            nurse_q_time_str = st.selectbox(
                'How often do nurse rounds occur (hosptials usually do every 1 or 2 hours)?', ('1 hour', '2 hours', '3 hours', '4 hours', '6 hours'), 
                index=1,
                key="nurse_freq"
            )
            nurse_q_hours = int(nurse_q_time_str.split(" ")[0])

            nurse_hourly_value = st.slider(
                "Value of 1 extra hour of nurse time. (Note that the average total hourly wage, including overhead, is $41).", 
                0, 45, 16, 
                key='nurse_cost'
            )

            number_of_nurse_rounds_per_unit_per_day = hours_per_day / nurse_q_hours
            nurse_minutes_saved_per_year_per_unit = mins_saved_per_round * number_of_nurse_rounds_per_unit_per_day * days_per_year 
            nurse_hours_saved_per_year_per_unit = nurse_minutes_saved_per_year_per_unit / minutes_per_hour
            nurse_hours_saved_per_year_per_facility = nurse_hours_saved_per_year_per_unit * number_of_units
            expected_savings_nurses = round(nurse_hours_saved_per_year_per_facility * nurse_hourly_value)

            t = f"""
            CALCULATIONS
            Minutes saved per round: {mins_to_complete_round} * {time_savings_perc / 100} = {round(mins_saved_per_round,1)}
            Number of rounds per unit per day: {hours_per_day} / {nurse_q_hours} = {int(number_of_nurse_rounds_per_unit_per_day)}
            Hours saved per unit per year: ({round(mins_saved_per_round,1)} / 60) * {int(number_of_nurse_rounds_per_unit_per_day)} * 365  = {round(nurse_hours_saved_per_year_per_unit,1)}
            Hours saved per facility per year: {round(nurse_hours_saved_per_year_per_unit,1)} * {number_of_units} = {round(nurse_hours_saved_per_year_per_facility,1)}
            Dollars saved per year = {round(nurse_hours_saved_per_year_per_facility, 1):,} * ${nurse_hourly_value} = ${expected_savings_nurses:,}
            """
            st.text(t)

if nurses_do_rounding:
    st.markdown(f"`{int(round(nurse_hours_saved_per_year_per_facility, 0)):,}` saved nurse hours per year at ${nurse_hourly_value} value per hour = `${expected_savings_nurses:,}` saved per year.")
else:
    expected_savings_nurses = 0
    st.markdown("Savings: not applicable")

st.write(" ")
st.write(" ")
st.write(" ")


with st.beta_expander("Paper Management Reduction"):
    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])

    with slider_col:
        txt = """
        Part of the reason to move to digital documentation is because of the cost of maintaining a paper system. These costs include: 
        * The paper, printers, and ink
        * Paper distribution and filing
        * Either scanning and uploading, or searching for records as needed
        """
        st.warning(txt)
        st.write(" ")

        paper_cost = st.slider("Cost per year for paper management.", 0, 30000, 12000, 1000)

expected_savings_paper = paper_cost        
st.markdown(f"Expected savings = `${expected_savings_paper:,}` per year.")

st.write(" ")
st.write(" ")
st.write(" ")

with st.beta_expander("Reduced Risk and Cost of Adverse Events"):

    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])

    with slider_col:  

        txt = """
        Adverse patient events can incur different and multiple costs, depending on their severity: 
        * The time it takes for internal review
        * The time and cost of external review and plans of correction
        * Impacts on survey and the potential for citation
        * Litigation costs, and impacts on liability insurance rates
        * Impact on hospital reputation and ability to recruit patients / fill beds
        """
        st.warning(txt)
        st.success("When facilities use our software system, compliance rates quickly increase to approximately 99%. The addition of automated verification ensures that all staff, regardless of time of day, are visiting each patient in person.")
        st.markdown("Please estimate the average annual cost of adverse events in your facility, taking into account that low-acuity events happen relatively frequently and that high-acuity events can have economic impacts in millions of dollars.")
        st.write(" ")

        adverse_cost = st.slider("Total average annual $ cost of adverse patient events", 0, 1000000, 100000, 10000)
        if include_verification:
            risk_reduction = st.slider("Estimated % risk reduction from 99% compliance and automated proximity verification for all safety checks.", 0, 100, 90, 5)
        else:
            risk_reduction = st.slider("Estimated % risk reduction from 99% safety rounding compliance", 0, 100, 50, 5)

        st.write(" ")
        t = f"""
        CALCULATIONS
        Reduction: {adverse_cost} * {risk_reduction / 100} = {int(adverse_cost * risk_reduction / 100):,}
        """
        st.text(t)        

expected_cost_reduction_adverse = adverse_cost * risk_reduction / 100
st.markdown(f"Expected reduction in cost due to adverse events = `${int(expected_cost_reduction_adverse):,}`")

st.write(" ")
st.write(" ")

st.sidebar.header("Facility ROI")
if include_verification:
    cost = 65 * num_facility_patients * 12
else:
    cost = 25 * num_facility_patients * 12
if include_verification:
    txt = f"Annual recurring cost of VisibleHand digital rounding and verification system = **${cost:,}**"
else:
    txt = f"Annual recurring cost of VisibleHand digital rounding system = **${cost:,}**"

sc1, sc2 = st.sidebar.beta_columns([0.5, 0.5])

total_savings = expected_savings_staff + expected_savings_nurses + expected_savings_paper + expected_cost_reduction_adverse

sc1.markdown("Annual cost:")
sc2.markdown(f"`${cost:,}`")

sc1.markdown("Annual savings:")
sc2.markdown(f"`${int(total_savings):,}`")

sc1.markdown("Difference:")
sc2.markdown(f"`${int(total_savings - cost):,}`")






