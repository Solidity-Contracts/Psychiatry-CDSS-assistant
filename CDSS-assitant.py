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

if not API_KEY:
    st.error("API key not found. Please check your secrets.toml file.")
else:
    client = OpenAI(api_key=API_KEY)

# Custom CSS for styling
st.markdown("""
    <style>
        body { background-color: #F4F4F4; }
        .highlight { background-color: #E8F5E9; padding: 10px; border-radius: 5px; }
        .center-button { display: flex; justify-content: center; }
    </style>
""", unsafe_allow_html=True)

# Title and Subtitle
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>LLM-Powered Clinical Decision Support for Psychiatrists</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>Using Maudsley Guidelines, DSM-5 & ICD-11 for Evidence-Based Recommendations</h4>", unsafe_allow_html=True)

# Initialize session state for patient history
if "patient_history" not in st.session_state:
    st.session_state.patient_history = []

# Input Section
st.markdown("### Patient Symptoms & Clinical History")

symptom_category = st.selectbox("Select Symptom Category:", [
    "Mood Disorders", "Anxiety Disorders", "Psychotic Disorders",
    "Neurodevelopmental Disorders", "Substance Use Disorders",
    "Trauma and Stressor-Related Disorders", "Personality Disorders",
    "Cognitive Disorders", "Other"
])

symptom_options = {
    "Mood Disorders": ["Persistent sadness", "Loss of interest", "Insomnia", "Hypersomnia"],
    "Anxiety Disorders": ["Excessive worry", "Panic attacks", "Hypervigilance"],
    "Psychotic Disorders": ["Hallucinations", "Delusions", "Disorganized speech"],
    "Other": ["Other symptom 1", "Other symptom 2"]
}

symptoms = st.multiselect("Select Symptoms:", symptom_options.get(symptom_category, []))
severity = st.radio("Select Severity:", ["Mild", "Moderate", "Severe"])
medical_history = st.text_area("Past Medical & Psychiatric History (Optional):")
medications = st.text_area("Current Medications & Past Treatments (Optional):")

st.markdown("---")
st.markdown("<h3 style='text-align: center;'>Get AI-Powered Recommendations</h3>", unsafe_allow_html=True)

# Centering the button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Generate Recommendations"):
        if not symptoms:
            st.error("Please select at least one symptom.")
        else:
            with st.spinner("Analyzing data... Generating recommendations..."):
                prompt = f"""
                You are an AI-powered clinical assistant for psychiatrists.
                Based on DSM-5, Maudsley Prescribing Guidelines, and ICD-11, provide:
                - Likely Diagnosis
                - Differential Diagnoses
                - Clinical Reasoning
                - Recommended Treatment Plan
                - ICD-11 Code
                - Any Red Flags Requiring Urgent Referral

                Patient Info:
                - Symptoms: {', '.join(symptoms)}
                - Severity: {severity}
                - Medical History: {medical_history if medical_history else 'Not provided'}
                - Medications: {medications if medications else 'Not provided'}
                """

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                recommendations = response.choices[0].message.content
                st.session_state.patient_history.append({"role": "AI", "content": recommendations})

            st.markdown("---")
            st.markdown("<h2 style='text-align: center;'>AI-Powered Recommendations</h2>", unsafe_allow_html=True)
            st.success("Analysis Complete!")

            sections = [
                "Likely Diagnosis",
                "Differential Diagnoses",
                "Clinical Reasoning",
                "Recommended Treatment Plan",
                "ICD-11 Code",
                "Red Flags Requiring Urgent Referral"
            ]

            for section in sections:
                start = recommendations.find(section)
                end = recommendations.find("\n", start) if start != -1 else None
                content = recommendations[start:end].strip() if start != -1 else "No information available."
                st.markdown(f"### {section}")
                st.markdown(f"<div class='highlight'>{content}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<h3 style='text-align: center;'>Ask Follow-Up Questions</h3>", unsafe_allow_html=True)

follow_up_question = st.text_input("Ask a question about the recommendations:")
if follow_up_question:
    with st.spinner("Generating response..."):
        st.session_state.patient_history.append({"role": "Doctor", "content": follow_up_question})
        follow_up_prompt = f"The doctor asks: {follow_up_question}\nProvide a clear and concise response."
        follow_up_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": follow_up_prompt}]
        )
        follow_up_answer = follow_up_response.choices[0].message.content
        st.session_state.patient_history.append({"role": "AI", "content": follow_up_answer})

    st.markdown("---")
    st.markdown("<h4 style='text-align: center;'>Follow-Up Response</h4>", unsafe_allow_html=True)
    st.write(follow_up_answer)

st.markdown("---")
st.markdown("<h3 style='text-align: center;'>Patient History</h3>", unsafe_allow_html=True)

for entry in st.session_state.patient_history:
    st.markdown(f"**{entry['role']}:** {entry['content']}")
