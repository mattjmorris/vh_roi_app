import streamlit as st
import math

st.set_page_config(    
    page_title="VisibleHand Return On Investment Calculator",
    page_icon="✋"
)

minutes_per_hour = 60
hours_per_day = 24
days_per_year = 365

st.title("[VisibleHand](https://www.visiblehand.com/) Return On Investment")
st.write(" ")



# ================= Sidebar ===================
s = """
## Directions

1. Enter basic info below.

2. Click on "+"s to the right to view and **modify** assumptions.

3. See values update in real-time.
"""
st.sidebar.info(s)

st.sidebar.write(" ")

_, slider_col, _ = st.sidebar.columns([0.1, 0.70, 0.1])
with slider_col:
    st.write("Number of Patients")
    num_facility_patients = st.number_input('How many patients?', value=100, step=10, format='%d')
    st.write(" ")
    st.write("Current Performance")
    current_compliance = st.select_slider("Staff complete their rounds with PERFECT compliance and proximity:", ["Sometimes", "Half of the Time", "Almost Always"], "Half of the Time")
    
    st.write(" ")
    include_verification = True 

#==============================================


with st.expander("Number of units and the time it takes to complete rounds.", False):

    _, slider_col, _ = st.columns([0.02, 0.96, 0.02])

    with slider_col:

        default_num_units = int(math.ceil(num_facility_patients / 20))
        max = max(20, (default_num_units+10))
        number_of_units = st.slider('Total Number of Units', 1, max, default_num_units)
        st.write(" ")
        patients_per_unit = int(math.ceil(num_facility_patients / number_of_units))
        if patients_per_unit <= 5:
            default_time = 3
            t = f"We find doing PERFECT rounding on paper with approximately {patients_per_unit} patients in a unit takes about {default_time} minutes."
        elif patients_per_unit <= 10:
            default_time = 6
            t = f"We find doing PERFECT rounding on paper with approximately {patients_per_unit} patients in a unit takes about {default_time} minutes."
        elif patients_per_unit <= 15:
            default_time = 11
            t = f"We find doing PERFECT rounding on paper with approximately {patients_per_unit} patients in a unit takes about {default_time} minutes."  
        elif patients_per_unit <= 20:
            default_time = 13
            t = f"We find doing PERFECT rounding on paper with approximately {patients_per_unit} patients in a unit takes about {default_time} minutes."   
        elif patients_per_unit <= 25:
            default_time = 15
            t = f"We find doing PERFECT rounding on paper with approximately {patients_per_unit} patients in a unit takes about {default_time} minutes."  
        else:
            default_time = 17
            t = f"We find doing PERFECT rounding on paper with approximately {patients_per_unit} patients in a unit takes at least {default_time} minutes."                                                 
        st.info(t)
        mins_to_complete_round = st.slider('Average # of minutes it takes to complete a PERFECT round with paper.', 3, 20, default_time)
        st.write(" ")


st.markdown(f"**{number_of_units}** units, **{mins_to_complete_round}** minutes on average to complete perfect rounds.")

st.write(" ")
st.write(" ")
st.write(" ")


with st.expander("Impact on Health Tech efficiency", False):

    _, slider_col, _ = st.columns([0.02, 0.96, 0.02])

    with slider_col:  
        staff_q_time_str = st.selectbox(
            'How often staff rounds occur at your facility', ('15 minutes', '30 minutes', '60 minutes', '90 minutes', '120 minutes')
        )
        staff_q_time = int(staff_q_time_str.split(" ")[0])

        st.write(" ")
        if current_compliance == "Sometimes":
            t = """
            If your staff are only 'Sometimes' following best practices, our system will help ensure that compliance quickly increases.
            However, you will not likely see a decrease in the time it takes health techs to do their rounds as they become more diligent about observing each and every patient. 
            """
            default = 0
            st.warning(t)
        elif current_compliance == "Half of the Time":
            t = """
            Because your staff are already doing about half of their rounds with full compliance, you can expect about a 10% decrease in the time it takes staff to complete rounds. 
            Doing rounds well will go faster but some health techs will be learning to be more diligent about observing every patient.
            """    
            default = 10   
            st.success(t)
        else:
            t = """
            If your staff are already following best practices, you can expect to see about a 40% decrease in the time it takes for them
            to complete rounds, thanks to our digital rounding app which has been optimized for speed and efficiency. 
            """
            default = 40
            st.success(t)
        
        time_savings_perc = st.slider(
            'Expected % time savings from transitioning to digital rounds.', 
            0, 60, default, 5
        )     
 
        st.write(" ")

        tt = """
        The average hourly cost of a health tech worker, including 25% overhead, is about $17.5 an hour.
        If your state allows adjusting of staff ratios, saving an hour of health tech time is worth close to the full hourly cost.
        Otherwise, its worth is based on the value of the additional tasks that health tech staff perform.
        We start off assuming that saving 1 hour of health tech time is worth $14 to you.
        """
        if current_compliance == "Sometimes":
            st.warning(tt)
        else:
            st.success(tt)

        staff_hourly_value = st.slider(
            "Value of 1 extra hour of health tech time at your facility.", 
            0, 20, 14
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


with st.expander("Impact on Nurse efficiency"):
    _, slider_col, _ = st.columns([0.02, 0.96, 0.02])

    with slider_col:    
        nurses_do_rounding = st.checkbox("Nurses do safety rounds (and review staff rounds)", True)
        if nurses_do_rounding:

            nurse_q_time_str = st.selectbox(
                'How often do nurse rounds occur (hosptials usually do every 1 or 2 hours)?', ('1 hour', '2 hours', '3 hours', '4 hours', '6 hours'), 
                index=1,
                key="nurse_freq"
            )
            nurse_q_hours = int(nurse_q_time_str.split(" ")[0])
            st.write(" ")

            if current_compliance == "Sometimes":
                t = """
                If your staff are only 'Sometimes' following best practices, our system will help ensure that compliance quickly increases.
                However, you will not likely see a decrease in the time it takes nurses to do their rounds as they become more diligent about observing each and every patient
                as well as reviewing health tech documentation. 
                """
                nurse_default = 0
                st.warning(t)
            elif current_compliance == "Half of the Time":
                t = """
                Nurses save at least as much time as staff during their rounds, and usually more because reviewing staff observations is many times faster with our app than with paper.
                If your staff are already doing about half of their rounds with full compliance, you can expect at least a 10% decrease in the time it takes nurses to complete rounds. 
                """    
                nurse_default = 10   
                st.success(t)
            else:
                t = """
                Nurses save at least as much time as staff during their rounds, and usually more because reviewing staff observations is many times faster with our app than with paper.
                If your staff are already following best practices, you can expect to see at least a 40% decrease in the time it takes for nurses
                to complete rounds. 
                """
                nurse_default = 40
                st.success(t)
            
            nurse_time_savings_perc = st.slider(
                'Expected % time savings from transitioning to digital rounds.', 
                0, 60, default, 5,
                key='nurse_time_savings'
            )     
    
            st.write(" ")

            ttt = """
            The average hourly cost of a nurse, including 25% overhead, is about $45 an hour.
            The value of a saved hour of nurse time at your facility will vary based on the value of the other tasks that nurses perform.
            We start off with a conservative assumption of $30 value per saved hour.
            """
            if current_compliance == "Sometimes":
                st.warning(ttt)
            else:
                st.success(ttt)

            nurse_hourly_value = st.slider(
                "Value of 1 extra hour of nurse time at your facility.", 
                0, 55, 30, 
                key='nurse_cost'
            )

            number_of_nurse_rounds_per_unit_per_day = hours_per_day / nurse_q_hours
            nurse_mins_saved_per_round = mins_to_complete_round * nurse_time_savings_perc / 100
            nurse_minutes_saved_per_year_per_unit = nurse_mins_saved_per_round * number_of_nurse_rounds_per_unit_per_day * days_per_year 
            nurse_hours_saved_per_year_per_unit = nurse_minutes_saved_per_year_per_unit / minutes_per_hour
            nurse_hours_saved_per_year_per_facility = nurse_hours_saved_per_year_per_unit * number_of_units
            expected_savings_nurses = round(nurse_hours_saved_per_year_per_facility * nurse_hourly_value)

            t = f"""
            CALCULATIONS
            Minutes saved per round: {mins_to_complete_round} * {nurse_time_savings_perc / 100} = {round(nurse_mins_saved_per_round,1)}
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


with st.expander("Paper Management Reduction"):
    _, slider_col, _ = st.columns([0.02, 0.96, 0.02])

    with slider_col:
        txt = f"""
        Part of the reason to move to digital documentation is because of the cost of maintaining a paper system. These costs include: 
        * The paper, printers, and ink
        * Paper distribution and filing
        * Either scanning and uploading, or searching for records as needed

        Based on feedback from customers, we estimate a total cost of $10 per bed per month, which comes to ${120 * num_facility_patients:,} per year for {num_facility_patients} patients
        """
        st.warning(txt)
        st.write(" ")
        
        default = int(120 * num_facility_patients)
        max = int(default + 10000)
        paper_cost = st.slider("Cost per year for paper management at your facility.", 0, max, default, 1000)

expected_savings_paper = paper_cost        
st.markdown(f"Expected savings = `${expected_savings_paper:,}` per year.")

st.write(" ")
st.write(" ")
st.write(" ")

with st.expander("Reduced Risk and Cost of Adverse Events"):

    _, slider_col, _ = st.columns([0.02, 0.96, 0.02])

    with slider_col:  

        txt = """
        Adverse patient events can incur different and multiple costs, depending on their severity: 
        * The time it takes for internal review
        * The time and cost of external review and plans of correction
        * Impacts on survey and the potential for citation
        * Litigation costs, and impacts on liability insurance rates
        * Impact on hospital reputation and ability to recruit patients / fill beds

        Facilities with low risk tend to experience costs in the thousands of dollars.

        Facilities with high risk have reported costs and losses exceeding one million dollars per year.
        """
        st.warning(txt)

        if current_compliance == "Sometimes":
            amount = 6000
            txt2 = f"""
            You indicated that your staff currently perform perfect rounds only {current_compliance}.
            This likely means that you have a higher annual risk and potential cost from adverse events.
            We estimate a risk adjusted average cost of ${amount:,} per bed per year, or ${amount * num_facility_patients:,} for your facility.
            """
            default_rc = amount * num_facility_patients
        elif current_compliance == "Half of the Time":
            amount = 3000
            txt2 = f"""
            You indicated that your staff currently perform perfect rounds {current_compliance}.
            This likely means that you have a moderate annual risk and potential cost from adverse events.
            We estimate a risk adjusted average cost of ${amount:,} per bed per year, or ${amount * num_facility_patients:,} for your facility.
            """
            default_rc = amount * num_facility_patients
        else:
            amount = 200
            txt2 = f"""
            You indicated that your staff currently perform perfect rounds {current_compliance}.
            This likely means that you have a lower annual risk and potential cost from adverse events.
            We estimate a risk adjusted average cost of ${amount:,} per bed per year, or ${amount * num_facility_patients:,} for your facility.
            """
            default_rc = int(amount * num_facility_patients)

        st.info(txt2)    

        st.markdown("The estimated average annual cost of adverse events in your facility.")
        st.write(" ")

        min = int(0)
        max = int(default_rc + 1000000)
        default_rc = int(default_rc)
        step = int(10000)
        adverse_cost = st.slider("Total average annual $ cost of adverse patient events for your facility", min, max, default_rc, step)
        
        tc = "When facilities use our digital rounding system, compliance rates quickly increase to approximately 99+%."
        tp = "The addition of automated verification ensures that all staff, regardless of time of day, are visiting each patient in person."

        if current_compliance == "Sometimes":
            if not include_verification:
                txt3 = f"""
                When facilities use our digital rounding system, compliance rates quickly increase to approximately 99+%.

                You are not including proximity verification.

                Given that your staff only perform perfect rounds {current_compliance}, we estimate a large improvement in compliance will reduce your risk by 60% compared to current levels.
                """
                risk_reduction_default = 60
            else:
                txt3 = f"""
                When facilities use our digital rounding system, compliance rates quickly increase to approximately 99+%.

                You are including proximity verification.

                Given that your staff only perform perfect rounds {current_compliance}, we estimate a large improvement in compliance PLUS quality will reduce your risk by 95% compared to current levels.
                """
                risk_reduction_default = 95                
        elif current_compliance == "Half of the Time":
            if not include_verification:
                txt3 = f"""
                When facilities use our digital rounding system, compliance rates quickly increase to approximately 99+%.

                You are not including proximity verification.

                Given that your staff only perform perfect rounds {current_compliance}, we estimate a sizeable improvement in compliance will reduce your risk by 50% compared to current levels.
                """
                risk_reduction_default = 50
            else:
                txt3 = f"""
                When facilities use our digital rounding system, compliance rates quickly increase to approximately 99+%.

                You are including proximity verification.

                Given that your staff only perform perfect rounds {current_compliance}, we estimate a sizeable improvement in compliance PLUS quality will reduce your risk by 80% compared to current levels.
                """
                risk_reduction_default = 80      
        else:
            if not include_verification:
                txt3 = f"""
                When facilities use our digital rounding system, compliance rates quickly increase to approximately 99+%.
                
                You are not including proximity verification.
                
                Given that your staff perform perfect rounds {current_compliance}, we estimate a small but real improvement in compliance will reduce your risk by 15% compared to current levels.
                """
                risk_reduction_default = 15
            else:
                txt3 = f"""
                When facilities use our digital rounding system, compliance rates quickly increase to approximately 99+%.

                You are including proximity verification.

                Given that your staff perform perfect rounds {current_compliance}, we estimate a small but real improvement in compliance AND quality will reduce your risk by 25% compared to current levels.
                """
                risk_reduction_default = 25  
    

        st.success(txt3)                   

        if include_verification:
            risk_reduction = st.slider("Estimated % risk reduction from 99+% compliance and automated proximity verification for all safety checks.", 0, 100, risk_reduction_default, 5)
        else:
            risk_reduction = st.slider("Estimated % risk reduction from 99+% safety rounding compliance", 0, 100, risk_reduction_default, 5)

        st.write(" ")
        t = f"""
        CALCULATIONS
        Reduction: {adverse_cost} * {risk_reduction / 100} = {int(adverse_cost * risk_reduction / 100):,}
        """
        st.text(t)        

expected_cost_reduction_adverse = adverse_cost * risk_reduction / 100
st.markdown(f"Expected annual reduction in cost due to adverse events = `${int(expected_cost_reduction_adverse):,}`")

# st.write("------")
total_savings = expected_savings_staff + expected_savings_nurses + expected_savings_paper + expected_cost_reduction_adverse
# st.subheader("Total annual expected savings")
# st.markdown(f"`${int(expected_savings_staff):,}` + `${int(expected_savings_nurses):,}` + `${int(expected_savings_paper):,}` + `${int(expected_cost_reduction_adverse):,}` = `${int(total_savings):,}`")

# ================= Sidebar ===================

st.sidebar.title("Results")
exculsive = st.sidebar.checkbox("Use $45/bed pricing for exclusive + contract")

if exculsive:
    costVHBed = 45.0
else:
    costVHBed = 0
    if num_facility_patients < 251:
        costVHBed = 58.5
    elif num_facility_patients < 501:
        costVHBed = 57.5
    elif num_facility_patients < 1001:
        costVHBed = 55
    elif num_facility_patients < 2501:
        costVHBed = 52.5
    elif num_facility_patients < 5001:
        costVHBed = 50.0
    elif num_facility_patients < 10001:
        costVHBed = 47.50
    else:
        costVHBed = 45.0
cost = costVHBed * num_facility_patients * 12


txt = f"Annual recurring cost of VisibleHand digital rounding and verification system = **${cost:,}**"


sc1, sc2 = st.sidebar.columns([0.5, 0.5])

sc1.markdown("Annual subscription:")
sc2.markdown(f"`${cost:,}`")

sc1.markdown("Annual savings:")
sc2.markdown(f"`${int(total_savings):,}`")

sc1.markdown("Difference:")
sc2.markdown(f"`${int(total_savings - cost):,}`")
#==============================================





