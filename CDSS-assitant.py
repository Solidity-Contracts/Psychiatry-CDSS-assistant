import os
import streamlit as st
from openai import OpenAI

# Configure the page layout
st.set_page_config(
    page_title="AI-Powered Psychiatric Assistant",
    page_icon="🧠",
    layout="wide"
)

# Access the OpenAI API key from secrets
API_KEY = st.secrets["API_KEY"]

if API_KEY is None:
    st.error("🚨 API key not found. Please check your secrets.toml file.")
else:
    st.success("✅ API key loaded successfully.")
    client = OpenAI(api_key=API_KEY)

# Custom CSS for Chat UI
st.markdown("""
    <style>
        body { background-color: #222; color: #ddd; }
        .stButton>button { background-color: #4CAF50; color: white; font-size: 18px; border-radius: 10px; }
        .stTextArea textarea, .stTextInput input { font-size: 16px; color: white; background-color: #333; }
        .stChatMessage { font-size: 16px; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
        .userMessage { background-color: #444; color: white; text-align: right; }
        .aiMessage { background-color: #2E86C1; color: white; text-align: left; }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #2E86C1; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🧠 AI Psychiatric Clinical Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #bbb;'>Standardizing Clinical Decision-Making in Psychiatry</h4>", unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
st.markdown("### 💬 Chat with the AI Clinical Assistant")
user_input = st.text_input("Ask about a patient's condition, guidelines, or treatment recommendations:")

if user_input:
    # Store user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare AI prompt
    chat_context = """
    You are an AI clinical assistant specializing in psychiatry. You provide evidence-based recommendations following DSM-5 and ICD-10 guidelines.
    You answer like a clinical consultant, offering structured responses in this format:
    
    **1. Likely Diagnosis**  
    **2. Differential Diagnoses**  
    **3. Clinical Reasoning**  
    **4. Recommended Treatment Plan (Medication + Therapy)**  
    **5. ICD-10 Code**  
    **6. Any Red Flags Requiring Urgent Referral**  

    If the user asks a general psychiatry question, provide an educational response.
    """

    # Fetch AI response
    full_conversation = [{"role": "system", "content": chat_context}] + st.session_state.chat_history
    response = client.chat.completions.create(model="gpt-4", messages=full_conversation)
    ai_response = response.choices[0].message.content

    # Store AI response
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div class='stChatMessage userMessage'>👨‍⚕️ **You:** {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='stChatMessage aiMessage'>🤖 **AI Assistant:** {msg['content']}</div>", unsafe_allow_html=True)
