import os
import streamlit as st
from openai import OpenAI

# Access the OpenAI API key from the environment variable
API_KEY = st.secrets["API_KEY"]

if API_KEY is None:
    st.error("API key not found. Please check your secrets.toml file.")
else:
    st.success("API key loaded successfully.")
    client = OpenAI(api_key=API_KEY)

# Streamlit App Title with LLM
st.title("LLM-Powered Clinical Decision Support for Psychiatrists")

# Input Section
st.header("Patient Symptoms")

# Step 1: Select Symptom Category
symptom_category = st.selectbox(
    "Select Symptom Category:",
    ["Mood Disorders", "Anxiety Disorders", "Psychotic Disorders", "Other"]
)

# Step 2: Select Specific Symptoms
if symptom_category == "Mood Disorders":
    symptoms = st.multiselect(
        "Select Symptoms:",
        ["Persistent sadness", "Loss of interest", "Fatigue", "Insomnia", "Feelings of worthlessness"]
    )
elif symptom_category == "Anxiety Disorders":
    symptoms = st.multiselect(
        "Select Symptoms:",
        ["Excessive worry", "Restlessness", "Fatigue", "Difficulty concentrating", "Irritability"]
    )
elif symptom_category == "Psychotic Disorders":
    symptoms = st.multiselect(
        "Select Symptoms:",
        ["Hallucinations", "Delusions", "Disorganized speech", "Disorganized behavior", "Negative symptoms"]
    )
else:
    symptoms = st.multiselect(
        "Select Symptoms:",
        ["Other symptom 1", "Other symptom 2", "Other symptom 3"]
    )

# Step 3: Add Additional Notes (Optional)
additional_notes = st.text_area("Additional Notes (Optional):", height=50)

# Button to Generate Recommendations
if st.button("Get Recommendations"):
    if not symptoms:
        st.error("Please select at least one symptom.")
    else:
        with st.spinner("Generating recommendations..."):
            # Prepare the prompt for the LLM
            prompt = f"""
            You are a clinical assistant for psychiatrists. Based on the DSM-5 and Maudsley guidelines, provide the following:
            1. Diagnosis
            2. Reasoning
            3. Treatment Plan
            4. ICD-10 Code

            Patient Symptoms: {", ".join(symptoms)}
            Additional Notes: {additional_notes}
            """
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or "gpt-3.5-turbo"
                messages=[{"role": "user", "content": prompt}]
            )
            recommendations = response['choices'][0]['message']['content']

        # Display Recommendations
        st.header("Recommendations")
        st.write(recommendations)
