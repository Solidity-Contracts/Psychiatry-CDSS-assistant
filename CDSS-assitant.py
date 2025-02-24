import streamlit as st
from openai import OpenAI

# Configure the page layout
st.set_page_config(
    page_title="AI-Powered Psychiatric Assistant",
    page_icon="🧠",
    layout="wide"
)

# Access the OpenAI API key from the environment variable
API_KEY = st.secrets["API_KEY"]

if API_KEY is None:
    st.error("API key not found. Please check your secrets.toml file.")
else:
    client = OpenAI(api_key=API_KEY)

# Custom CSS for a professional look
st.markdown("""
    <style>
        body { background-color: #F4F4F4; }
        .stButton>button { background-color: #4CAF50; color: white; font-size: 16px; }
        .stTextArea textarea { font-size: 14px; }
        .stSelectbox select { font-size: 14px; }
        .stMultiselect div { font-size: 14px; }
        .stRadio div { font-size: 14px; }
        .stHeader { font-size: 20px; font-weight: bold; color: #333366; }
    </style>
""", unsafe_allow_html=True)

# Title and Subtitle
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>LLM-Powered Clinical Decision Support for Psychiatrists</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>Using Maudsley Guidelines, DSM-5 & ICD-10 for Evidence-Based Recommendations</h4>", unsafe_allow_html=True)

# Initialize session state for patient history
if "patient_history" not in st.session_state:
    st.session_state.patient_history = []

# Input Section
st.markdown("### Patient Symptoms & Clinical History")

# Step 1: Select Symptom Category
st.markdown("#### 1. Select Symptom Category")
symptom_category = st.selectbox(
    "Choose a Category:",
    [
        "Mood Disorders", "Anxiety Disorders", "Psychotic Disorders",
        "Personality Disorders", "Neurodevelopmental Disorders",
        "Substance Use Disorders", "Dementia & Cognitive Disorders", "Other"
    ]
)

# Step 2: Select Specific Symptoms
st.markdown("#### 2. Select Specific Symptoms")
symptom_options = {
    "Mood Disorders": [
        "Persistent sadness", "Loss of interest", "Insomnia", "Hypersomnia",
        "Weight loss/gain", "Feelings of worthlessness", "Suicidal ideation"
    ],
    "Anxiety Disorders": [
        "Excessive worry", "Panic attacks", "Hypervigilance",
        "Obsessive thoughts", "Compulsive behaviors"
    ],
    "Psychotic Disorders": [
        "Hallucinations", "Delusions", "Disorganized speech", "Disorganized behavior"
    ],
    "Personality Disorders": [
        "Unstable relationships", "Self-harm", "Grandiosity", "Fear of abandonment"
    ],
    "Neurodevelopmental Disorders": [
        "Inattention", "Hyperactivity", "Impulsivity", "Repetitive behaviors"
    ],
    "Substance Use Disorders": [
        "Cravings", "Withdrawal symptoms", "Drug-seeking behavior"
    ],
    "Dementia & Cognitive Disorders": [
        "Memory loss", "Disorientation", "Language impairment"
    ],
    "Other": ["Other symptom 1", "Other symptom 2"]
}

symptoms = st.multiselect("Choose Symptoms:", symptom_options.get(symptom_category, []))

# Step 3: Select Symptom Severity
st.markdown("#### 3. Select Symptom Severity")
severity = st.radio("Choose Severity:", ["🟢 Mild", "🟡 Moderate", "🔴 Severe"])

# Step 4: Additional Clinical Information
st.markdown("#### 4. Add Additional Clinical Information")
medical_history = st.text_area("Past Medical & Psychiatric History (Optional):")
medications = st.text_area("Current Medications & Past Treatments (Optional):")

# Button to Generate Recommendations
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>Get AI-Powered Recommendations</h3>", unsafe_allow_html=True)

if st.button("Generate Recommendations"):
    if not symptoms:
        st.error("Please select at least one symptom.")
    else:
        with st.spinner("Analyzing data... Generating recommendations..."):
            # Prepare the prompt for the LLM
            prompt = f"""
            You are an AI-powered clinical assistant for psychiatrists. 
            Based on the DSM-5, Maudsley Prescribing Guidelines, and ICD-10 codes, 
            provide a structured response including:

            1. Likely Diagnosis  
            2. Differential Diagnoses  
            3. Clinical Reasoning  
            4. Recommended Treatment Plan (Based on Maudsley Guidelines)  
            5. ICD-10 Code  
            6. Any Red Flags Requiring Urgent Referral  

            Patient Information:  
            - Symptoms: {", ".join(symptoms)}  
            - Severity: {severity}  
            - Medical History: {medical_history if medical_history else 'Not provided'}  
            - Current Medications: {medications if medications else 'Not provided'}  

            Provide a detailed and structured response.
            """
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            recommendations = response.choices[0].message.content

            # Save the initial recommendations to patient history
            st.session_state.patient_history.append({"role": "AI", "content": recommendations})

        # Display Recommendations
        st.markdown("---")
        st.markdown("<h2 style='text-align: center;'>AI-Powered Recommendations</h2>", unsafe_allow_html=True)
        st.success("Analysis Complete!")
        st.write(recommendations)

# Chatbot-Like Interaction for Follow-Up Questions
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>Ask Follow-Up Questions</h3>", unsafe_allow_html=True)

follow_up_question = st.text_input("Ask a question about the recommendations:")
if follow_up_question:
    with st.spinner("Generating response..."):
        # Add the follow-up question to patient history
        st.session_state.patient_history.append({"role": "Doctor", "content": follow_up_question})

        # Prepare the follow-up prompt
        follow_up_prompt = f"""
        The doctor has asked the following question about your recommendations:
        {follow_up_question}

        Please provide a detailed and clear response.
        """
        follow_up_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": follow_up_prompt}]
        )
        follow_up_answer = follow_up_response.choices[0].message.content

        # Save the follow-up response to patient history
        st.session_state.patient_history.append({"role": "AI", "content": follow_up_answer})

    # Display Follow-Up Response
    st.markdown("---")
    st.markdown("<h4 style='text-align: center;'>Follow-Up Response</h4>", unsafe_allow_html=True)
    st.write(follow_up_answer)

# Display Patient History
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>Patient History</h3>", unsafe_allow_html=True)
for entry in st.session_state.patient_history:
    if entry["role"] == "AI":
        st.markdown(f"**AI:** {entry['content']}")
    else:
        st.markdown(f"**Doctor:** {entry['content']}")
