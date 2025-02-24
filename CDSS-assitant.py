import os
import streamlit as st
from openai import OpenAI
import base64
from datetime import datetime

# Configure the page layout
st.set_page_config(
    page_title="AI-Powered Psychiatric Assistant",
    page_icon="🧠",
    layout="wide"
)

# Access the OpenAI API key from the environment variable
API_KEY = st.secrets["API_KEY"]

if API_KEY is None:
    st.error("🚨 API key not found. Please check your secrets.toml file.")
else:
    client = OpenAI(api_key=API_KEY)

# Custom CSS for UI Enhancement
st.markdown("""
    <style>
        body { background-color: #F4F4F4; }
        .stButton>button { background-color: #4CAF50; color: white; font-size: 18px; }
        .stTextArea textarea { font-size: 16px; }
        .stSelectbox select { font-size: 16px; }
        .stMultiselect div { font-size: 16px; }
        .stRadio div { font-size: 16px; }
        .stHeader { font-size: 24px; font-weight: bold; color: #333366; }
    </style>
""", unsafe_allow_html=True)

# Title and Subtitle
st.markdown(
    "<h1 style='text-align: center; color: #2E86C1;'>🧠 AI-Powered Clinical Decision Support for Psychiatrists</h1>", 
    unsafe_allow_html=True
)
st.markdown(
    "<h4 style='text-align: center; color: #555;'>Using Maudsley Guidelines, DSM-5 & ICD-10 for Evidence-Based Recommendations</h4>", 
    unsafe_allow_html=True
)
# Input Section
st.markdown("### 📋 Enter Patient Symptoms & Clinical History")

# Step 1: Select Symptom Category
st.markdown("#### 1️⃣ Select Symptom Category")
symptom_category = st.selectbox(
    "Choose a Category:",
    [
        "Mood Disorders", "Anxiety Disorders", "Psychotic Disorders",
        "Personality Disorders", "Neurodevelopmental Disorders",
        "Substance Use Disorders", "Dementia & Cognitive Disorders", "Other"
    ]
)

# Step 2: Select Specific Symptoms with collapsible sections
st.markdown("#### 2️⃣ Select Specific Symptoms")
symptom_options = {
    "Mood Disorders": [
        "😞 Persistent sadness", "😶 Loss of interest", "😴 Insomnia", "💤 Hypersomnia",
        "⚖️ Weight loss/gain", "😔 Feelings of worthlessness", "🚨 Suicidal ideation"
    ],
    "Anxiety Disorders": [
        "😰 Excessive worry", "😵 Panic attacks", "⚡ Hypervigilance",
        "🤯 Obsessive thoughts", "🔄 Compulsive behaviors"
    ],
    "Psychotic Disorders": [
        "👂 Hallucinations", "🌀 Delusions", "🗣️ Disorganized speech", "🚶‍♂️ Disorganized behavior"
    ],
    "Personality Disorders": [
        "🎭 Unstable relationships", "🔪 Self-harm", "🌀 Grandiosity", "🚨 Fear of abandonment"
    ],
    "Neurodevelopmental Disorders": [
        "⏳ Inattention", "⚡ Hyperactivity", "📣 Impulsivity", "🤖 Repetitive behaviors"
    ],
    "Substance Use Disorders": [
        "🍷 Cravings", "⚠️ Withdrawal symptoms", "🚨 Drug-seeking behavior"
    ],
    "Dementia & Cognitive Disorders": [
        "🧠 Memory loss", "🧩 Disorientation", "🔠 Language impairment"
    ],
    "Other": ["❓ Other symptom 1", "❓ Other symptom 2"]
}

with st.expander("Click to Select Symptoms", expanded=True):
    symptoms = st.multiselect("Choose Symptoms:", symptom_options.get(symptom_category, []))

# Step 3: Select Symptom Severity
st.markdown("#### 3️⃣ Select Symptom Severity")
severity = st.radio("Choose Severity:", ["🟢 Mild", "🟡 Moderate", "🔴 Severe"])

# Step 4: Additional Clinical Information
st.markdown("#### 4️⃣ Add Additional Clinical Information")
medical_history = st.text_area("📝 Past Medical & Psychiatric History (Optional):")
medications = st.text_area("💊 Current Medications & Past Treatments (Optional):")

# Button to Generate Recommendations
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>🚀 Get AI-Powered Recommendations</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🧠 Generate Recommendations", use_container_width=True):
        if not symptoms:
            st.error("❌ Please select at least one symptom.")
        else:
            with st.spinner("🔍 Analyzing data... Generating recommendations..."):
                # Prepare the prompt for the LLM
                prompt = f"""
                You are an AI-powered clinical assistant for psychiatrists. 
                Based on the DSM-5, Maudsley guidelines, and ICD-10 codes, 
                provide a structured response including:

                **1. Likely Diagnosis**  
                **2. Differential Diagnoses**  
                **3. Clinical Reasoning**  
                **4. Recommended Treatment Plan (Medication + Therapy)**  
                **5. ICD-10 Code**  
                **6. Any Red Flags Requiring Urgent Referral**  

                **Patient Information:**  
                - **Symptoms:** {", ".join(symptoms)}  
                - **Severity:** {severity}  
                - **Medical History:** {medical_history if medical_history else 'Not provided'}  
                - **Current Medications:** {medications if medications else 'Not provided'}  

                Provide a detailed and structured response.
                """
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                recommendations = response.choices[0].message.content

            # Display Recommendations
            st.markdown("---")
            st.markdown("<h2 style='text-align: center;'>📜 AI-Powered Recommendations</h2>", unsafe_allow_html=True)
            st.success("✅ Analysis Complete!")

            # Allow doctors to edit the recommendations
            st.markdown("#### ✏️ Edit Recommendations (if needed)")
            edited_recommendations = st.text_area("Edit the recommendations below:", value=recommendations, height=400)

            # Save or export the recommendations
            st.markdown("#### 💾 Save or Export Recommendations")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Save to Patient Record"):
                    # Simulate saving to a database or EHR
                    st.success("✅ Recommendations saved to patient record.")
            with col2:
                # Export as PDF
                pdf_data = base64.b64encode(edited_recommendations.encode()).decode()
                pdf_download_link = f'<a href="data:application/pdf;base64,{pdf_data}" download="recommendations.pdf">📄 Download as PDF</a>'
                st.markdown(pdf_download_link, unsafe_allow_html=True)

            # Feedback Section
            st.markdown("#### 📝 Provide Feedback")
            feedback = st.radio("Was this recommendation helpful?", ["👍 Yes", "👎 No"])
            if feedback == "👎 No":
                feedback_details = st.text_area("Please provide additional details:")
                if st.button("Submit Feedback"):
                    st.success("✅ Thank you for your feedback! We'll use it to improve the system.")
