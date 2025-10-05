import streamlit as st
import pandas as pd
from PIL import Image
import smtplib
import csv
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="NeuroBlast Onboarding",
    page_icon="logos/NeuroBlast_logo.png",
    layout="wide"
)

# --- App Title and Introduction ---
st.markdown("<h1 style='text-align: center;'>NeuroBlast Program Implementation: Academy Onboarding Questionnaire</h1>", unsafe_allow_html=True)

target_height = 100
col1, col2, col3 = st.columns(3)
with col1:
    image = Image.open("logos/CENABH_Logo.png")
    new_width = int(image.width * (target_height / image.height))
    resized_image = image.resize((new_width, target_height))
    st.image(resized_image)
with col2:
    image = Image.open("logos/NeuroBlast_logo.png")
    new_width = int(image.width * (target_height / image.height))
    resized_image = image.resize((new_width, target_height))
    st.image(resized_image)
with col3:
    image = Image.open("logos/Synaptom logo.png")
    new_width = int(image.width * (target_height / image.height))
    resized_image = image.resize((new_width, target_height))
    st.image(resized_image)

st.markdown("""
Thank you for your interest in implementing the **NeuroBlast Program**. NeuroBlast is a pioneering sports performance program that combines cutting-edge brain science with practical athletic training. The program is an initiative of **SynaptOm Pvt. Ltd.**, developed in close collaboration with our primary knowledge partner, the **Centre of Excellence in Neurodegeneration and Brain Health (CENABH)** at Cochin University of Science and Technology (CUSAT). It also incorporates international expertise through collaboration with Croatian experts.

This questionnaire is designed to help us understand your academy's unique structure and requirements. Your detailed responses are crucial for us to tailor the program effectively, ensure a smooth implementation, and prepare an accurate financial budget proposal.
""")

# --- Create a dictionary to hold all form data ---
form_data = {}

# --- Form Sections ---

# --- Section 1: General Academy Information ---
st.header("Part 1: General Academy Information")
form_data['academy_name'] = st.text_input("Full Name of the Academy *")

col1, col2 = st.columns(2)
with col1:
    form_data['contact_name'] = st.text_input("Primary Contact Person - Name *")
    form_data['contact_email'] = st.text_input("Primary Contact Person - Email *")
with col2:
    form_data['contact_designation'] = st.text_input("Primary Contact Person - Designation *")
    form_data['contact_phone'] = st.text_input("Primary Contact Person - Phone Number *")
    
form_data['main_location'] = st.text_area("Location of Main Training Facility / Stadium *")

remote_centers = st.radio("Do you have any remote or sub-centers? *", ("No", "Yes"), horizontal=True)
if remote_centers == "Yes":
    form_data['remote_locations'] = st.text_area("If yes, please list their locations:")

st.divider()

# --- Section 2: Details of Students / Players ---
st.header("Part 2: Details of Students / Players")
form_data['total_students'] = st.number_input("Total Number of Students currently enrolled in the academy *", min_value=0, step=1)
form_data['age_group'] = st.text_input("Overall Age Group of Students (e.g., from 8 to 19 years) *")

st.markdown("##### Batch Details *")
# Using st.data_editor for a table-like input
df = pd.DataFrame(
    [
        {"Batch Name / ID": "e.g., U-15 Boys", "No. of Players": 25, "Gender": "Boys", "Age Group": "14-15", "Level of Training": "Intermediate", "Avg. Duration (Months)": 2.0, "Fee (₹ *Not Mandatory)": 0, "Unit": "Per Month"},
    ]
)
form_data['batch_details'] = st.data_editor(
    df,
    column_config={
        "Gender": st.column_config.SelectboxColumn(
            "Gender",
            help="The gender of the batch",
            width="medium",
            options=[
                "Boys",
                "Girls",
                "Mixed",
            ],
            required=True,
        ),
        "Level of Training": st.column_config.SelectboxColumn(
            "Level of Training",
            help="The level of training of the batch",
            width="medium",
            options=[
                "Beginner",
                "Basic",
                "Intermediate",
                "Professional",
            ],
            required=True,
        ),
        "Fee": st.column_config.NumberColumn(
            "Fee (INR)",
            help="The fee for the batch in Rupees",
            min_value=0,
            format="%d",
        ),
        "Unit": st.column_config.SelectboxColumn(
            "Unit",
            help="The fee unit",
            width="medium",
            options=[
                "Per Month",
                "Per Course",
                "Per Week",
                "Per Session",
                "Per Year",
            ],
            required=True,
        ),
    },
    num_rows="dynamic",
    use_container_width=True
)

st.divider()

# --- Section 3: Details of Facilities & Staff ---
st.header("Part 3: Details of Facilities & Staff")
expertise_options = ["Football Coach (UEFA/AFC Certified)", "Team Physician (Doctor)", "Physiotherapist", "Sports Psychologist", "General Psychologist / Counselor", "Nutritionist / Dietitian"]
form_data['in_house_expertise'] = st.multiselect("In-House Expertise (Select all that apply) *", expertise_options)
form_data['other_expertise'] = st.text_input("Other expertise (please specify):")

form_data['player_coach_ratio'] = st.text_input("Player to Coach Ratio (for on-field training) *")
special_equipment_options = [
        "Video analysis cameras (VAR)",
        "GPS player trackers",
        "Performance analysis software",
        "Training cones",
        "Speed ladders",
        "Agility hurdles",
        "Tackle dummies",
        "Blocking sleds",
        "Free-kick wall mannequins",
        "Rebounders",
        "Weighted sleds",
        "Resistance bands"
    ]
form_data['special_equipment'] = st.multiselect("Special Training Equipment", options=special_equipment_options, help="Select any special training equipment you use.")
form_data['custom_special_equipment'] = st.text_area("Other special training equipment (please specify):")

dedicated_space = st.radio("Is there a dedicated space for NeuroBlast's cognitive training sessions? *", ("No", "Yes"), horizontal=True)
if dedicated_space == "Yes":
    form_data['dedicated_space_desc'] = st.text_area("If yes, please describe it briefly (e.g., capacity, equipment available):")

form_data['internet'] = st.radio("Is reliable Wi-Fi available at the training facility/dedicated space? *", ("No", "Yes"), horizontal=True)

st.divider()

# --- Section 4: Training Program Details ---
st.header("Part 4: Training Program Details")
nature_of_training = st.radio("Nature of Training *", ("Residential (Players live at the academy)", "Weekly Training (Non-Residential)"), horizontal=True)
form_data['nature_of_training'] = nature_of_training

if nature_of_training == "Weekly Training (Non-Residential)":
    st.markdown("##### Weekly Training Schedule")
    col3, col4 = st.columns(2)
    with col3:
        form_data['training_days'] = st.multiselect("Days:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    with col4:
        form_data['training_timings'] = st.text_input("Timings (e.g., 4 PM - 6 PM):")

form_data['training_hours_per_day'] = st.number_input("Hours of on-field training per training day *", min_value=0.0, step=0.5)
form_data['parental_involvement'] = st.text_area("Parental Involvement", help="How are parents typically involved (e.g., regular meetings, progress reports, observation of sessions, etc.)?")

use_digital = st.radio("Does the academy currently use any digital platform (app/website)? *", ("No", "Yes"), horizontal=True)
if use_digital == "Yes":
    form_data['digital_platform_desc'] = st.text_area("If yes, please describe briefly:")
    
form_data['online_training'] = st.radio("Is any mode of training currently given online? *", ("No", "Yes"), horizontal=True)
form_data['device_access'] = st.selectbox("Do students generally have access to a mobile device? *", ("Unsure", "Yes, most do", "No, access is limited"))

st.divider()

# --- Section 5: Suggestions & Expectations ---
st.header("Part 5: Suggestions & Expectations from Team SynaptOm")
familiarity = st.radio("Have you come across neuroscience-based training methods before? *", ("No", "Yes"), horizontal=True)
if familiarity == "Yes":
    form_data['familiarity_desc'] = st.text_area("If yes, please share briefly:")

primary_goals_options = [
    "Improve tactical decision-making",
    "Enhance on-field focus",
    "Better reaction time",
    "Increase stress tolerance",
    "Reduce match-day anxiety",
    "Improve emotional regulation",
    "Improve mental speed",
    "Boost player memory for game plans",
    "Improve problem-solving abilities",
    "Boost overall player self-confidence",
    "Improve post-game mental recovery",
    "Enhance motor co-ordination and movement quality",
    "Optimize movement efficiency",
    "Boost overall energy levels",
    "Improve player well-being outside of football",
    "Foster better team cohesion"
]
form_data['primary_goals'] = st.multiselect("Primary Goals for NeuroBlast *", options=primary_goals_options)
form_data['custom_goals'] = st.text_area("Other primary goals (please specify):")

col5, col6 = st.columns(2)
with col5:
    form_data['target_group'] = st.text_input("Target age group or team for the initial program *")
with col6:
    form_data['target_group_size'] = st.number_input("Total number of students in this target group *", min_value=0, step=1)

form_data['specific_details'] = st.text_area("Specific Details to Highlight", help="Any challenges, strengths, or other details about your academy or this target group you would like us to know?")
form_data['further_questions'] = st.text_area("Further Questions", help="Any initial questions for us or specific areas where you require more clarity about the program?")

st.markdown("""
**Privacy and Data Use Disclaimer**

By submitting this form, you acknowledge and agree to the following:

The information you provide will be used by SynaptOm Pvt. Ltd. and its authorized partners for the purpose of tailoring the NeuroBlast Program, preparing a financial budget proposal, and for program implementation.

All personal data will be handled with the utmost care and confidentiality. Your information will only be accessible to authorized personnel and will not be shared with any third party without your prior explicit consent. Anonymized data may be used for research and program improvement purposes.
""")

# --- Submit Button ---
submitted = st.button("Submit Details")


# --- Post-Submission Logic ---
if submitted:
    mandatory_fields = {
        'academy_name': "Full Name of the Academy",
        'contact_name': "Primary Contact Person - Name",
        'contact_email': "Primary Contact Person - Email",
        'contact_designation': "Primary Contact Person - Designation",
        'contact_phone': "Primary Contact Person - Phone Number",
        'main_location': "Location of Main Training Facility / Stadium",
        'total_students': "Total Number of Students",
        'age_group': "Overall Age Group of Students",
        'in_house_expertise': "In-House Expertise",
        'player_coach_ratio': "Player to Coach Ratio",
        'training_hours_per_day': "Hours of on-field training per training day",
        'primary_goals': "Primary Goals for NeuroBlast",
        'target_group': "Target age group or team for the initial program",
        'target_group_size': "Total number of students in this target group"
    }
    
    missing_fields = []
    for field_key, field_name in mandatory_fields.items():
        if not form_data.get(field_key):
            missing_fields.append(field_name)

    if missing_fields:
        st.error(f"Please fill in all mandatory fields. The following fields are missing: {', '.join(missing_fields)}")
    else:
        # --- Create CSV in memory ---
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        for key, value in form_data.items():
            writer.writerow([key, value])
        csv_buffer.seek(0)

        # --- Email Logic ---
        try:
            # --- Email Configuration (IMPORTANT: Fill in your details in the .env file) ---
            smtp_server = os.getenv("SMTP_SERVER")
            smtp_port = int(os.getenv("SMTP_PORT"))
            smtp_user = os.getenv("SMTP_USER")
            smtp_password = os.getenv("SMTP_PASSWORD")

            from_email = smtp_user
            to_emails = ["info@synaptom.com", "synaptomofficial@gmail.com", "info@nvisust.com"]

            # --- Create Email ---
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = ", ".join(to_emails)
            msg['Subject'] = f"New NeuroBlast Onboarding Submission: {form_data.get('academy_name', 'N/A')}"

            # --- Email Body ---
            body = "A new academy has submitted the NeuroBlast onboarding questionnaire. The details are attached as a CSV file."
            msg.attach(MIMEText(body, 'plain'))

            # --- Attach CSV ---
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(csv_buffer.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename=submission_{form_data.get('academy_name', 'N/A').replace(' ', '_')}.csv")
            msg.attach(part)

            # --- Send Email ---
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, to_emails, msg.as_string())
            
            st.toast("Your submission has been received!", icon="🎉")

        except Exception as e:
            st.error(f"An error occurred while sending the email: {e}")
            st.warning("Please save a copy of your responses below.")

        # --- Display Summary ---
        st.subheader("Summary of Your Responses:")
        for key, value in form_data.items():
            if key == "batch_details":
                st.markdown(f"**Batch Details:**")
                st.dataframe(value)
            elif value:
                st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
